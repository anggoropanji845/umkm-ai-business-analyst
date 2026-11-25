from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output
from lfx.schema.message import Message

import csv
import io
import json
import pandas as pd


class UMKMDataAnalyzer(Component):
    display_name = "UMKM Data Analyzer"
    description = "Calculate validated business KPIs and descriptive segments from UMKM e-commerce CSV data."
    icon = "chart"
    name = "UMKMDataAnalyzer"

    inputs = [
        MessageTextInput(
            name="csv_data",
            display_name="CSV Data",
            info="CSV text received from the Read File component.",
            required=True,
        ),
    ]

    outputs = [
        Output(
            display_name="Business Analysis",
            name="analysis",
            method="build_analysis",
        ),
    ]

    @staticmethod
    def _detect_separator(raw_csv: str) -> str:
        sample = "\n".join(
            line for line in raw_csv.splitlines()[:20] if line.strip()
        )
        try:
            return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
        except csv.Error:
            first_line = next((line for line in raw_csv.splitlines() if line.strip()), "")
            counts = {sep: first_line.count(sep) for sep in [",", ";", "\t", "|"]}
            return max(counts, key=counts.get)

    @staticmethod
    def _safe_int(value):
        return int(value) if pd.notna(value) else 0

    def build_analysis(self) -> Message:
        raw_csv = self.csv_data
        if not raw_csv or not str(raw_csv).strip():
            raise ValueError("CSV kosong. Pastikan Read File mengirim isi file CSV.")

        separator = self._detect_separator(str(raw_csv))
        df = pd.read_csv(io.StringIO(str(raw_csv)), sep=separator)

        required = [
            "order_id", "Status Pesanan", "Total Pembayaran",
            "product_categories", "order_date"
        ]
        missing_columns = [col for col in required if col not in df.columns]
        if missing_columns:
            raise ValueError(
                "Kolom wajib tidak ditemukan setelah parsing CSV. "
                f"Separator terdeteksi={repr(separator)}; "
                f"kolom terbaca={df.columns.tolist()}; "
                f"kolom yang dibutuhkan={missing_columns}. "
                "Periksa apakah Read File mengirim CSV utuh dan delimiter-nya benar."
            )

        df = df.copy()
        df["order_id"] = df["order_id"].astype("string").str.strip()
        df["status_raw"] = df["Status Pesanan"].astype("string").str.strip()
        df["status_normalized"] = df["status_raw"].mask(
            df["status_raw"].str.startswith(
                "Pesanan diterima, namun Pembeli masih dapat mengajukan pengembalian",
                na=False,
            ),
            "Dalam Masa Pengembalian",
        )

        df["Total Pembayaran"] = pd.to_numeric(
            df["Total Pembayaran"], errors="coerce"
        )
        if "total_qty" in df.columns:
            df["total_qty"] = pd.to_numeric(df["total_qty"], errors="coerce")

        # Prefer order_date; use creation timestamp only as a row-level fallback.
        df["order_date_parsed"] = pd.to_datetime(
            df["order_date"], errors="coerce"
        )
        timestamp_col = "Waktu Pesanan Dibuat"
        if timestamp_col in df.columns:
            df["created_at_parsed"] = pd.to_datetime(
                df[timestamp_col], errors="coerce"
            )
            recoverable = (
                df["order_date_parsed"].isna()
                & df["created_at_parsed"].notna()
            )
            df["analysis_date"] = df["order_date_parsed"].fillna(
                df["created_at_parsed"]
            )
            both_dates = (
                df["order_date_parsed"].notna()
                & df["created_at_parsed"].notna()
            )
            date_mismatch_count = int(
                (
                    df.loc[both_dates, "order_date_parsed"].dt.date
                    != df.loc[both_dates, "created_at_parsed"].dt.date
                ).sum()
            )
        else:
            recoverable = pd.Series(False, index=df.index)
            df["analysis_date"] = df["order_date_parsed"]
            date_mismatch_count = None

        total_orders = int(df["order_id"].nunique())
        completed = df[df["status_normalized"].eq("Selesai")]
        cancelled = df[df["status_normalized"].eq("Batal")]
        completed_payments = completed["Total Pembayaran"].dropna()

        completed_orders = int(completed["order_id"].nunique())
        cancelled_orders = int(cancelled["order_id"].nunique())
        cancellation_rate = (
            cancelled_orders / total_orders * 100 if total_orders else None
        )

        # AOV is calculated only for completed orders; mean and median are both returned.
        aov_mean = (
            float(completed_payments.mean())
            if not completed_payments.empty else None
        )
        aov_median = (
            float(completed_payments.median())
            if not completed_payments.empty else None
        )

        # Monthly series is reindexed so months with zero orders remain explicit.
        monthly_records = []
        dated = df.dropna(subset=["analysis_date"]).copy()
        if not dated.empty:
            dated["order_month"] = dated["analysis_date"].dt.to_period("M")
            monthly = dated.groupby("order_month").agg(
                total_orders=("order_id", "nunique"),
                completed_orders=(
                    "status_normalized", lambda s: int(s.eq("Selesai").sum())
                ),
                cancelled_orders=(
                    "status_normalized", lambda s: int(s.eq("Batal").sum())
                ),
            )
            full_months = pd.period_range(
                monthly.index.min(), monthly.index.max(), freq="M"
            )
            monthly = monthly.reindex(full_months, fill_value=0)
            for month, row in monthly.iterrows():
                n = int(row["total_orders"])
                monthly_records.append({
                    "month": str(month),
                    "total_orders": n,
                    "completed_orders": int(row["completed_orders"]),
                    "cancelled_orders": int(row["cancelled_orders"]),
                    "cancellation_rate_pct": (
                        round(int(row["cancelled_orders"]) / n * 100, 2)
                        if n else None
                    ),
                })

        def grouped_cancellation(column, min_n=1, limit=15):
            if column not in df.columns:
                return []
            temp = df[["order_id", "status_normalized", column]].copy()
            temp[column] = (
                temp[column].astype("string").fillna("Unknown").str.strip()
            )
            grouped = temp.groupby(column, dropna=False).agg(
                total_orders=("order_id", "nunique"),
                cancelled_orders=(
                    "status_normalized", lambda s: int(s.eq("Batal").sum())
                ),
            )
            grouped["cancellation_rate_pct"] = (
                grouped["cancelled_orders"] / grouped["total_orders"] * 100
            )
            grouped = grouped[grouped["total_orders"] >= min_n]
            grouped = grouped.sort_values(
                ["cancellation_rate_pct", "total_orders"],
                ascending=[False, False],
            ).head(limit)
            return [
                {
                    "group": str(index),
                    "total_orders": int(row["total_orders"]),
                    "cancelled_orders": int(row["cancelled_orders"]),
                    "cancellation_rate_pct": round(
                        float(row["cancellation_rate_pct"]), 2
                    ),
                }
                for index, row in grouped.iterrows()
            ]

        # Cancellation reasons are meaningful only within cancelled orders.
        reason_counts = []
        if "Alasan Pembatalan" in df.columns:
            reason_counts = [
                {"reason": str(reason), "cancelled_orders": int(count)}
                for reason, count in
                cancelled["Alasan Pembatalan"].astype("string")
                .fillna("Unknown").str.strip().value_counts().head(15).items()
            ]

        # Split multi-category cells; count unique orders containing each category.
        category_counts = []
        if "product_categories" in df.columns:
            category_long = df[["order_id", "product_categories"]].copy()
            category_long["category"] = (
                category_long["product_categories"].astype("string")
                .str.split(r"\s*,\s*")
            )
            category_long = category_long.explode("category")
            category_long["category"] = category_long["category"].str.strip()
            category_long = category_long.dropna(subset=["category"])
            top_categories = (
                category_long.groupby("category")["order_id"]
                .nunique().sort_values(ascending=False).head(10)
            )
            category_counts = [
                {"category": str(category), "orders": int(count)}
                for category, count in top_categories.items()
            ]

        qty_missing = (
            int(df["total_qty"].isna().sum())
            if "total_qty" in df.columns else None
        )
        qty_mean = (
            float(df["total_qty"].mean())
            if "total_qty" in df.columns and df["total_qty"].notna().any()
            else None
        )
        unknown_payment_count = (
            int(
                df["Metode Pembayaran"].isna().sum()
                + df["Metode Pembayaran"].astype("string")
                .str.strip().str.lower().eq("unknown").sum()
            )
            if "Metode Pembayaran" in df.columns else None
        )

        result = {
            "project": "UMKM AI Business Analyst",
            "data_quality": {
                "total_records": int(len(df)),
                "unique_orders": total_orders,
                "duplicate_rows": int(df.duplicated().sum()),
                "duplicate_order_ids": int(df["order_id"].duplicated().sum()),
                "missing_values": {
                    str(k): int(v) for k, v in df.isna().sum().items()
                },
                "date_parse_failures": int(df["order_date_parsed"].isna().sum()),
                "date_recovered_from_created_at": int(recoverable.sum()),
                "date_mismatch_count": date_mismatch_count,
                "qty_missing_count": qty_missing,
            },
            "definitions": {
                "cancellation_rate": (
                    "cancelled unique orders / all unique orders * 100; "
                    "denominator includes every order status"
                ),
                "aov": (
                    "mean and median Total Pembayaran for orders with "
                    "Status Pesanan = Selesai only"
                ),
                "category_count": (
                    "number of unique orders containing each category after "
                    "splitting multi-category cells; not item quantity"
                ),
            },
            "kpis": {
                "total_orders": total_orders,
                "completed_orders": completed_orders,
                "cancelled_orders": cancelled_orders,
                "cancellation_rate_pct": (
                    round(cancellation_rate, 2)
                    if cancellation_rate is not None else None
                ),
                "completed_payment_sum": round(
                    float(completed_payments.sum()), 2
                ),
                "aov_mean_completed": (
                    round(aov_mean, 2) if aov_mean is not None else None
                ),
                "aov_median_completed": (
                    round(aov_median, 2) if aov_median is not None else None
                ),
                "average_qty_valid": (
                    round(qty_mean, 3) if qty_mean is not None else None
                ),
                "qty_missing_count": qty_missing,
                "unknown_payment_count": unknown_payment_count,
                "cancelled_orders_with_zero_payment": int(
                    cancelled["Total Pembayaran"].eq(0).sum()
                ),
            },
            "order_status": {
                str(k): int(v)
                for k, v in df["status_normalized"].value_counts().items()
            },
            "monthly_trend": monthly_records,
            "cancellation_by_payment_method_min_n_30": grouped_cancellation(
                "Metode Pembayaran", min_n=30, limit=15
            ),
            "cancellation_by_province_min_n_30": grouped_cancellation(
                "Provinsi", min_n=30, limit=15
            ),
            "cancellation_by_shipping_min_n_30": grouped_cancellation(
                "Opsi Pengiriman", min_n=30, limit=15
            ),
            "cancellation_reasons": reason_counts,
            "top_categories_by_unique_orders": category_counts,
        }

        return Message(
            text=json.dumps(result, ensure_ascii=False, default=str, indent=2)
        )
