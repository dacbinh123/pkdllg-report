import streamlit as st
import pandas as pd
import plotly.express as px  # Cần thiết để vẽ biểu đồ
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    FilterExpression,
    Filter,
)
from google_auth_oauthlib.flow import Flow 
import streamlit as st
from streamlit_oauth import OAuth2Component
import os
# =================================================================
# CHỖ ĐIỀN URL - BẠN TỰ FILL VÀO ĐÂY
# =================================================================

# 1. Nhóm TRỊ MỤN
URL_TRI_MUN = """
https://phongkhamdalieulg.vn/uong-bia-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-me-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-le-co-noi-mun-khong/
https://phongkhamdalieulg.vn/mun-trung-ca-do/
https://phongkhamdalieulg.vn/mun-tuoi-day-thi-co-tu-het-khong/
https://phongkhamdalieulg.vn/mun-trung-ca/
https://phongkhamdalieulg.vn/tri-mun-doctor-laser/
https://phongkhamdalieulg.vn/nen-boi-kem-tri-mun-truoc-hay-sau-duong-am/
https://phongkhamdalieulg.vn/quy-trinh-cham-soc-da-mun-hang-ngay/
https://phongkhamdalieulg.vn/mun-dau-den-co-nen-nan-khong/
https://phongkhamdalieulg.vn/mun-thit-la-gi/
https://phongkhamdalieulg.vn/dieu-tri-mun/
https://phongkhamdalieulg.vn/cham-soc-da-mun-dung-cach/
https://phongkhamdalieulg.vn/huong-dan-nan-mun-dau-den-o-mui/
https://phongkhamdalieulg.vn/13-spa-tri-mun-uy-tin-nhat-o-tphcm/
https://phongkhamdalieulg.vn/10-cach-tri-mun-bang-nha-dam/
https://phongkhamdalieulg.vn/dang-peel-da-co-dung-kem-chong-nang-duoc-khong/
https://phongkhamdalieulg.vn/lay-nhan-mun-co-tot-khong/
https://phongkhamdalieulg.vn/lot-mun-cam/
https://phongkhamdalieulg.vn/peel-da-tri-mun/
https://phongkhamdalieulg.vn/cach-tri-mun-bang-chanh/
https://phongkhamdalieulg.vn/bi-mun-noi-tiet-nen-uong-vitamin-gi/
https://phongkhamdalieulg.vn/uong-thuoc-tranh-thai-tri-mun-noi-tiet/
https://phongkhamdalieulg.vn/uong-vitamin-e-tri-mun-noi-tiet/
https://phongkhamdalieulg.vn/uong-gi-cho-mat-gan-het-mun/
https://phongkhamdalieulg.vn/peel-da-day-mun-trong-bao-lau/
https://phongkhamdalieulg.vn/mun-dau-den/
https://phongkhamdalieulg.vn/cach-uong-rau-ma-tri-mun/
https://phongkhamdalieulg.vn/mun-trung-ca-moc-quanh-mieng/
https://phongkhamdalieulg.vn/cach-tri-mun-trung-ca/
https://phongkhamdalieulg.vn/mun-an-duoi-cam/
https://phongkhamdalieulg.vn/uong-collagen-bi-noi-mun/
https://phongkhamdalieulg.vn/mun-trung-ca-ung/
https://phongkhamdalieulg.vn/cach-day-mun-an-ra-ngoai/
https://phongkhamdalieulg.vn/nguyen-nhan-gay-mun/
https://phongkhamdalieulg.vn/co-nen-nan-mun-trung-ca-khong/
https://phongkhamdalieulg.vn/tri-mun-bang-mat-ong-sau-1-dem/
https://phongkhamdalieulg.vn/cach-tri-mun-bang-khoai-tay/
https://phongkhamdalieulg.vn/xong-mat-bang-la-tia-to-tri-mun/
https://phongkhamdalieulg.vn/mun-boc-mu/
https://phongkhamdalieulg.vn/mun-boc-o-ma/
https://phongkhamdalieulg.vn/mun-an-co-nen-nan-khong/
https://phongkhamdalieulg.vn/thuoc-tri-mun-trung-ca/
https://phongkhamdalieulg.vn/mun-an-tren-tran/
https://phongkhamdalieulg.vn/mun-an-2-ben-ma/
https://phongkhamdalieulg.vn/cac-buoc-skincare-cho-da-dau-mun-an/
https://phongkhamdalieulg.vn/co-nen-nan-mun-an-o-spa/
https://phongkhamdalieulg.vn/cach-tri-mun-noi-tiet-dut-diem/
https://phongkhamdalieulg.vn/cach-tri-mun-noi-tiet-sau-sinh/
https://phongkhamdalieulg.vn/uong-kem-tri-mun-noi-tiet/
https://phongkhamdalieulg.vn/thuc-don-cho-nguoi-bi-mun-noi-tiet/
https://phongkhamdalieulg.vn/nuoc-ep-tri-mun-noi-tiet/
https://phongkhamdalieulg.vn/mun-cam-o-mui/
https://phongkhamdalieulg.vn/mun-noi-tiet-o-nu/
https://phongkhamdalieulg.vn/roi-loan-noi-tiet-to-nam-gay-mun/
https://phongkhamdalieulg.vn/tai-sao-triet-long-mat-lai-noi-mun/
https://phongkhamdalieulg.vn/uong-thuoc-tay-nhieu-bi-noi-mun-phai-lam-sao/
https://phongkhamdalieulg.vn/uong-thuoc-khang-sinh-bi-noi-mun/
https://phongkhamdalieulg.vn/mun-an-o-mui/
https://phongkhamdalieulg.vn/cach-su-dung-than-hoat-tinh-tay-mun-dau-den/
https://phongkhamdalieulg.vn/tri-mun-dau-den-o-mui-bang-vaseline/
https://phongkhamdalieulg.vn/peel-da-tri-mun-co-lam-mong-da-khong/
https://phongkhamdalieulg.vn/peel-da-tri-mun-xong-co-duoc-dung-tay-trang-khong/
https://phongkhamdalieulg.vn/dung-sua-rua-mat-bi-noi-mun/
https://phongkhamdalieulg.vn/deo-khau-trang-nhieu-co-bi-mun-khong/
https://phongkhamdalieulg.vn/mun-dau-trang/
https://phongkhamdalieulg.vn/mun-o-tran/
https://phongkhamdalieulg.vn/bi-mun-boc-kieng-an-gi/
https://phongkhamdalieulg.vn/mun-an-co-peel-da-duoc-khong/
https://phongkhamdalieulg.vn/co-nen-peel-da-sau-khi-nan-mun/
https://phongkhamdalieulg.vn/huong-dan-cham-soc-da-sau-peel-mun-theo-tung-giai-doan/
https://phongkhamdalieulg.vn/peel-da-khong-bong-co-tot-khong/
https://phongkhamdalieulg.vn/peel-da-bao-lau-thi-rua-mat/
https://phongkhamdalieulg.vn/mun-dau-den-va-soi-ba-nhon/
https://phongkhamdalieulg.vn/mun-dau-den-o-ma/
https://phongkhamdalieulg.vn/mun-dau-den-co-thanh-not-ruoi-khong/
https://phongkhamdalieulg.vn/mun-dau-den-co-tu-het-duoc-khong/
https://phongkhamdalieulg.vn/co-nen-lot-mun-dau-den-o-mui-khong/
https://phongkhamdalieulg.vn/tri-mun-dau-den-o-mui-tai-nha/
https://phongkhamdalieulg.vn/mun-do-stress/
https://phongkhamdalieulg.vn/luu-huynh-tri-mun/
https://phongkhamdalieulg.vn/mun-an-co-tu-het-khong/
https://phongkhamdalieulg.vn/mun-cam/
https://phongkhamdalieulg.vn/quy-trinh-tri-mun-tai-spa/
https://phongkhamdalieulg.vn/mun-o-quai-ham/
https://phongkhamdalieulg.vn/bi-mun-co-nen-an-rau-muong-khong/
https://phongkhamdalieulg.vn/kham-mun/
https://phongkhamdalieulg.vn/mun-chai/
https://phongkhamdalieulg.vn/mun-gao/
https://phongkhamdalieulg.vn/mun-o-long-may/
https://phongkhamdalieulg.vn/mun-trung-ca-nang/
https://phongkhamdalieulg.vn/mun-o-mong/
https://phongkhamdalieulg.vn/mun-trung-ca-co-mui-hoi/
https://phongkhamdalieulg.vn/spa-tri-mun-quan-tan-binh/
https://phongkhamdalieulg.vn/lam-sao-biet-minh-bi-mun-noi-tiet/
https://phongkhamdalieulg.vn/an-chom-chom-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-vai-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-dau-phong-co-noi-mun-khong/
https://phongkhamdalieulg.vn/thuc-khuya-co-noi-mun-khong/
https://phongkhamdalieulg.vn/mun-trung-ca-mu/
https://phongkhamdalieulg.vn/tri-mun-quan-10/
https://phongkhamdalieulg.vn/mun-trung-ca-o-tran/
https://phongkhamdalieulg.vn/mun-an/
https://phongkhamdalieulg.vn/mun-boc/
https://phongkhamdalieulg.vn/cach-chua-mun-di-ung-my-pham/
https://phongkhamdalieulg.vn/nguyen-nhan-mun-tai-di-tai-lai/
https://phongkhamdalieulg.vn/mun-tham-tu-mau-co-tu-het-khong/
https://phongkhamdalieulg.vn/mun-trung-ca-co-tu-het-khong/
https://phongkhamdalieulg.vn/an-dua-hau-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-dau-tay-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-xoi-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-trung-ca-co-noi-mun-khong/
https://phongkhamdalieulg.vn/bi-mun-nen-an-rau-gi/
https://phongkhamdalieulg.vn/an-gi-de-het-mun/
https://phongkhamdalieulg.vn/chua-mun-trung-ca-bang-rau-diep-ca/
https://phongkhamdalieulg.vn/nhung-mon-an-gay-mun-trung-ca/
https://phongkhamdalieulg.vn/an-hat-dieu-co-noi-mun-khong/
https://phongkhamdalieulg.vn/cach-tri-mun-bang-la-tia-to/
https://phongkhamdalieulg.vn/tri-mun-bang-long-trang-trung-ga/
https://phongkhamdalieulg.vn/cach-tri-mun-bang-ba-ca-phe/
https://phongkhamdalieulg.vn/bot-cam-gao-tri-mun/
https://phongkhamdalieulg.vn/cach-lam-mat-na-tri-mun-tai-nha/
https://phongkhamdalieulg.vn/vi-sao-dung-kem-chong-nang-bi-noi-mun/
https://phongkhamdalieulg.vn/an-luu-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-sau-rieng-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-mi-tom-co-moc-mun-khong/
https://phongkhamdalieulg.vn/an-nho-co-noi-mun-khong/
https://phongkhamdalieulg.vn/bi-mun-an-trung-duoc-khong/
https://phongkhamdalieulg.vn/uong-ca-phe-co-noi-mun-khong/
https://phongkhamdalieulg.vn/uong-vitamin-c-dhc-co-bi-noi-mun-khong/
https://phongkhamdalieulg.vn/uong-vitamin-e-co-bi-noi-mun-khong/
https://phongkhamdalieulg.vn/uong-thuoc-mat-gan-co-het-mun-khong/
https://phongkhamdalieulg.vn/mat-mun-co-nen-cao-long-mat-khong/
https://phongkhamdalieulg.vn/noi-mun-o-ma/
https://phongkhamdalieulg.vn/tretinoin-co-day-mun-khong/
https://phongkhamdalieulg.vn/vi-khuan-p-acnes/
https://phongkhamdalieulg.vn/mun-dau-dinh/
https://phongkhamdalieulg.vn/mun-nang/
https://phongkhamdalieulg.vn/an-coc-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-man-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-mi-cay-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-kem-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-mang-cut-co-noi-mun-khong/
https://phongkhamdalieulg.vn/mun-mu/
https://phongkhamdalieulg.vn/mun-o-bap-tay/
https://phongkhamdalieulg.vn/mun-viem/
https://phongkhamdalieulg.vn/cac-loai-mun-trung-ca/
https://phongkhamdalieulg.vn/bi-mun-co-nen-di-kham-da-lieu/
https://phongkhamdalieulg.vn/mun-dinh-rau-la-gi/
https://phongkhamdalieulg.vn/cach-tri-mun-viem-do-khong-nhan/
https://phongkhamdalieulg.vn/mun-nhot/
https://phongkhamdalieulg.vn/tri-mun-binh-duong/
https://phongkhamdalieulg.vn/spa-tri-mun-quan-binh-tan/
https://phongkhamdalieulg.vn/spa-tri-mun-tan-phu/
https://phongkhamdalieulg.vn/spa-tri-mun-go-vap/
https://phongkhamdalieulg.vn/tri-mun-o-binh-thanh/
https://phongkhamdalieulg.vn/uong-omega-3-co-bi-noi-mun-khong/
https://phongkhamdalieulg.vn/tri-mun-quan-1/
https://phongkhamdalieulg.vn/an-du-du-co-bi-noi-mun-hay-khong/
https://phongkhamdalieulg.vn/bi-mun-co-nen-an-sua-chua-khong/
https://phongkhamdalieulg.vn/an-tao-co-noi-mun-khong/
https://phongkhamdalieulg.vn/bang-gia-dieu-tri-mun/
https://phongkhamdalieulg.vn/bac-si-da-lieu-tri-mun-tphcm/
https://phongkhamdalieulg.vn/bi-mun-co-nen-an-thit-ga-khong/
https://phongkhamdalieulg.vn/an-cay-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-bo-co-noi-mun-khong/
https://phongkhamdalieulg.vn/mun-an-dung-aha-hay-bha/
https://phongkhamdalieulg.vn/mun-an-nen-dung-bha-hay-retinol/
https://phongkhamdalieulg.vn/mun-trung-ca-o-vung-kin/
https://phongkhamdalieulg.vn/l70-trung-ca/
https://phongkhamdalieulg.vn/cach-ngan-ngua-mun-trung-ca/
https://phongkhamdalieulg.vn/phat-ban-mun-trung-ca/
https://phongkhamdalieulg.vn/cach-tri-mun-trung-ca-o-tuoi-day-thi/
https://phongkhamdalieulg.vn/uong-isotretinoin-co-nen-nan-mun-khong/
https://phongkhamdalieulg.vn/lam-sao-de-khong-bi-mun-khi-den-thang/
https://phongkhamdalieulg.vn/day-mun/
https://phongkhamdalieulg.vn/mun-boc-o-cam/
https://phongkhamdalieulg.vn/mun-boc-o-mui/
https://phongkhamdalieulg.vn/mun-boc-co-tu-xep-khong/
https://phongkhamdalieulg.vn/cach-nan-mun-boc-khong-dau/
https://phongkhamdalieulg.vn/tri-mun-boc-o-mui-sau-1-dem/
https://phongkhamdalieulg.vn/an-thanh-long-co-noi-mun-khong/
https://phongkhamdalieulg.vn/mun-boc-bao-lau-thi-chin/
https://phongkhamdalieulg.vn/an-nhan-co-noi-mun-va-nong-trong-nguoi-khong/
https://phongkhamdalieulg.vn/peel-da-tri-mun-gia-bao-nhieu/
https://phongkhamdalieulg.vn/mun-cam-o-tran/
https://phongkhamdalieulg.vn/an-chuoi-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-oi-co-noi-mun-khong/
https://phongkhamdalieulg.vn/da-san-sui-mun-an/
https://phongkhamdalieulg.vn/peel-da-tri-mun-tai-nha/
https://phongkhamdalieulg.vn/peel-da-bi-do-rat/
https://phongkhamdalieulg.vn/peel-da-bi-noi-mun-nuoc/
https://phongkhamdalieulg.vn/an-banh-mi-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-banh-trang-co-noi-mun-khong/
https://phongkhamdalieulg.vn/mun-boc-o-tran/
https://phongkhamdalieulg.vn/cach-nan-mun-boc-bi-chai-cung/
https://phongkhamdalieulg.vn/bi-mun-co-nen-an-thit-bo-khong/
https://phongkhamdalieulg.vn/dung-bia-tri-mun/
https://phongkhamdalieulg.vn/an-do-chien-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-ngot-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-chua-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-bap-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-chao-goi-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-khoai-lang-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-dua-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-nhieu-man-co-noi-mun-khong/
https://phongkhamdalieulg.vn/cach-lam-nuoc-xong-mat-tri-mun-cho-da-nhon/
https://phongkhamdalieulg.vn/cach-dung-bia-de-tri-mun/
https://phongkhamdalieulg.vn/tri-mun-bang-khoai-tay/
https://phongkhamdalieulg.vn/tri-mun-bang-la-tia-to-hieu-qua/
https://phongkhamdalieulg.vn/an-mit-co-noi-mun-khong/
https://phongkhamdalieulg.vn/uong-nuoc-mia-co-noi-mun-khong/
https://phongkhamdalieulg.vn/bi-mun-trung-ca-nen-an-gi-va-kieng-gi/
https://phongkhamdalieulg.vn/tai-sao-cang-skincare-cang-len-mun/
https://phongkhamdalieulg.vn/boi-serum-bi-noi-mun/
https://phongkhamdalieulg.vn/an-socola-co-noi-mun-khong/
https://phongkhamdalieulg.vn/hinh-anh-mat-mun-tuoi-day-thi/
https://phongkhamdalieulg.vn/uong-thuoc-khang-sinh-tri-mun-co-tot-khong/
https://phongkhamdalieulg.vn/an-xoai-co-noi-mun-khong/
https://phongkhamdalieulg.vn/an-quyt-co-noi-mun-khong/
https://phongkhamdalieulg.vn/mun-li-ti/
https://phongkhamdalieulg.vn/mun-di-ung/
https://phongkhamdalieulg.vn/mun-mach-luon/
https://phongkhamdalieulg.vn/mun-o-nguc/
https://phongkhamdalieulg.vn/mun-o-cam/
https://phongkhamdalieulg.vn/cac-loai-mun-o-mui/
https://phongkhamdalieulg.vn/mun-trong-mui/
https://phongkhamdalieulg.vn/mun-o-co/
https://phongkhamdalieulg.vn/tri-mun/
https://phongkhamdalieulg.vn/tri-mun/ipl-tri-mun/
https://phongkhamdalieulg.vn/tri-mun/chieu-anh-sang-sinh-hoc-tri-mun/
https://phongkhamdalieulg.vn/tri-mun/kham-mun/
https://phongkhamdalieulg.vn/tri-mun/peel-da-tri-mun/
https://phongkhamdalieulg.vn/tri-mun/tiem-meso-tri-mun/
https://phongkhamdalieulg.vn/tri-mun/lay-nhan-mun/
https://phongkhamdalieulg.vn/tri-mun/laser-co2-fractional-tri-mun/
https://phongkhamdalieulg.vn/kien-thuc-tri-mun/
"""

# 2. Nhóm TRỊ NÁM
URL_TRI_NAM = """
https://phongkhamdalieulg.vn/dieu-tri-nam
https://phongkhamdalieulg.vn/dia-chi-tri-nam-uy-tin/
https://phongkhamdalieulg.vn/dieu-tri-nam-bang-laser-bao-nhieu-tien/
https://phongkhamdalieulg.vn/dieu-tri-nam-bang-laser-co-hieu-qua-khong/
https://phongkhamdalieulg.vn/xoa-tan-nhang-bang-laser-bao-nhieu-tien/
https://phongkhamdalieulg.vn/tri-nam-da-mat/
https://phongkhamdalieulg.vn/cach-tri-nam-sau-sinh/
https://phongkhamdalieulg.vn/peel-da-tri-nam/
https://phongkhamdalieulg.vn/cach-tri-nam-hieu-qua-nhat-hien-nay/
https://phongkhamdalieulg.vn/nam-dom/
https://phongkhamdalieulg.vn/nam-hori/
https://phongkhamdalieulg.vn/nam-mang/
https://phongkhamdalieulg.vn/tiem-meso-tri-nam/
https://phongkhamdalieulg.vn/cong-nghe-tri-nam-tot-nhat-hien-nay/
https://phongkhamdalieulg.vn/nam-nhe-2-ben-go-ma/
https://phongkhamdalieulg.vn/nguyen-nhan-nam-da-mat-o-nam-gioi/
https://phongkhamdalieulg.vn/nam-o-song-mui/
https://phongkhamdalieulg.vn/tri-nam-tan-nhang/
https://phongkhamdalieulg.vn/dau-hieu-bi-nam/
https://phongkhamdalieulg.vn/tri-nam-pico-melasma/
https://phongkhamdalieulg.vn/dieu-tri-nam-da/
https://phongkhamdalieulg.vn/nam-da/
https://phongkhamdalieulg.vn/cac-nguyen-nhan-gay-nam-da/
https://phongkhamdalieulg.vn/cach-tri-nam-rau/
https://phongkhamdalieulg.vn/nam-sau-sinh-co-tu-het-khong/
https://phongkhamdalieulg.vn/nam-canh-buom/
https://phongkhamdalieulg.vn/dieu-tri-nam-chan-dinh/
https://phongkhamdalieulg.vn/nam-chan-sau/
https://phongkhamdalieulg.vn/nam-doi-moi/
https://phongkhamdalieulg.vn/nam-da-quanh-mieng/
https://phongkhamdalieulg.vn/nam-da-mat/
https://phongkhamdalieulg.vn/nam-mang-va-nam-chan-sau/
https://phongkhamdalieulg.vn/tri-tan-nhang-bang-laser/
"""

# 3. Nhóm SẸO RỖ (Tách từ sẹo chung)
URL_SEO_RO = """
https://phongkhamdalieulg.vn/lieu-trinh-tri-seo-ro-bao-lau/
https://phongkhamdalieulg.vn/seo-ro-nang/
https://phongkhamdalieulg.vn/nguyen-nhan-gay-seo-ro/
https://phongkhamdalieulg.vn/seo-lom-lau-nam-co-tri-duoc-khong/
https://phongkhamdalieulg.vn/tri-seo-ro-bang-laser-co2-co-het-khong/
https://phongkhamdalieulg.vn/tri-seo-ro-bang-laser-co2-gia-bao-nhieu/
https://phongkhamdalieulg.vn/cach-tri-seo-ro-lau-nam-tren-mat-tai-nha/
https://phongkhamdalieulg.vn/peel-da-tri-seo-ro/
https://phongkhamdalieulg.vn/tiem-collagen-lam-day-seo-lom/
https://phongkhamdalieulg.vn/dia-chi-dieu-tri-seo-ro-tot-nhat-tphcm/
https://phongkhamdalieulg.vn/seo-ro-co-tu-het-khong/
https://phongkhamdalieulg.vn/lan-kim-tri-seo-ro/
https://phongkhamdalieulg.vn/tri-seo-ro-gia-bao-nhieu/
https://phongkhamdalieulg.vn/cat-day-seo-ro-gia-bao-nhieu/
https://phongkhamdalieulg.vn/cong-nghe-tri-seo-ro-tot-nhat-hien-nay/
https://phongkhamdalieulg.vn/xoa-seo-lom-moi-hinh-thanh/
https://phongkhamdalieulg.vn/tri-seo-ro-co-dau-khong/
https://phongkhamdalieulg.vn/tiem-meso-tri-seo-ro/
https://phongkhamdalieulg.vn/tri-seo-lom-lau-nam-tai-nha/
https://phongkhamdalieulg.vn/bi-seo-lom-co-nen-an-rau-muong/
https://phongkhamdalieulg.vn/tay-not-ruoi-bi-seo-lom-phai-lam-sao/
https://phongkhamdalieulg.vn/te-bao-goc-tri-seo-ro-tot-nhat-hien-nay/
https://phongkhamdalieulg.vn/mat-na-tri-seo-ro-lau-nam/
https://phongkhamdalieulg.vn/seo-ro-o-mui/
https://phongkhamdalieulg.vn/retinol-co-tri-seo-ro-khong/
https://phongkhamdalieulg.vn/tretinoin-tri-seo-ro/
https://phongkhamdalieulg.vn/te-bao-goc-tri-seo-ro/
https://phongkhamdalieulg.vn/seo-ro/
https://phongkhamdalieulg.vn/dieu-tri-seo-ro/
https://phongkhamdalieulg.vn/seo-ro-nhe/
https://phongkhamdalieulg.vn/cat-day-seo/
https://phongkhamdalieulg.vn/lan-kim-tri-seo-ro-gia-bao-nhieu/
https://phongkhamdalieulg.vn/seo-ro-co-tri-duoc-khong/
https://phongkhamdalieulg.vn/tri-seo-ro-moi-hinh-thanh/
https://phongkhamdalieulg.vn/cham-tca-tri-seo-ro/
https://phongkhamdalieulg.vn/cham-soc-da-bi-seo-ro/
https://phongkhamdalieulg.vn/dau-dua-tri-seo-ro/
https://phongkhamdalieulg.vn/tri-seo-ro-bang-mat-ong/
https://phongkhamdalieulg.vn/seo-lom/
https://phongkhamdalieulg.vn/tri-seo-lom/
https://phongkhamdalieulg.vn/tri-seo-ro-do-mun/
https://phongkhamdalieulg.vn/dieu-tri-seo-ro-bang-laser/
https://phongkhamdalieulg.vn/tri-seo-ro-cho-nam/
https://phongkhamdalieulg.vn/seo-ro-day-nhon/
https://phongkhamdalieulg.vn/seo-ro-day-tron/
https://phongkhamdalieulg.vn/seo-ro-day-vuong/
https://phongkhamdalieulg.vn/seo-lom-va-seo-ro-khac-nhau-nhu-the-nao/
https://phongkhamdalieulg.vn/seo-day-nhon-va-lo-chan-long-to/
https://phongkhamdalieulg.vn/phi-kim-tri-seo-ro/
https://phongkhamdalieulg.vn/seo-ro-luon-song/
https://phongkhamdalieulg.vn/kien-thuc-seo-ro/
"""

# 4. Nhóm SẸO LỒI (Tách từ sẹo chung)
URL_SEO_LOI = """
https://phongkhamdalieulg.vn/seo-loi-co-tu-het-khong/
https://phongkhamdalieulg.vn/seo-loi/
https://phongkhamdalieulg.vn/cach-tri-seo-loi-lau-nam/
https://phongkhamdalieulg.vn/an-tom-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-rau-lang-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/seo-loi-tu-moc/
https://phongkhamdalieulg.vn/kieng-an-gi-de-khong-bi-seo-loi/
https://phongkhamdalieulg.vn/cach-tri-seo-loi-tai-nha/
https://phongkhamdalieulg.vn/an-ngheu-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-ca-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-oc-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-muc-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-hai-san-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-mi-tom-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-xoi-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-trung-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-rau-muong-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-thit-de-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-thit-ga-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-thit-vit-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/an-thit-bo-co-bi-seo-loi-khong/
https://phongkhamdalieulg.vn/seo-loi-ngay-cang-to/
https://phongkhamdalieulg.vn/seo-loi-bi-ngua-phai-lam-sao/
https://phongkhamdalieulg.vn/seo-loi-bi-dau/
https://phongkhamdalieulg.vn/seo-loi-o-mui/
https://phongkhamdalieulg.vn/seo-loi-o-tai/
https://phongkhamdalieulg.vn/seo-loi-o-nguc/
https://phongkhamdalieulg.vn/cat-seo-loi/
https://phongkhamdalieulg.vn/tiem-seo-loi-bao-lau-thi-xep/
https://phongkhamdalieulg.vn/tiem-seo-loi/
https://phongkhamdalieulg.vn/cach-tri-seo-loi-moi-hinh-thanh/
https://phongkhamdalieulg.vn/tri-seo-loi-bang-cong-nghe-laser-co2-fractional/
https://phongkhamdalieulg.vn/tri-seo-loi-bang-nito-long/
https://phongkhamdalieulg.vn/tri-seo-loi-bang-laser-gia-bao-nhieu/
https://phongkhamdalieulg.vn/dia-chi-tiem-seo-loi/
"""

# 5. Nhóm MỤN LƯNG
URL_MUN_LUNG = """
https://phongkhamdalieulg.vn/kien-thuc-mun-lung/
https://phongkhamdalieulg.vn/baking-soda-tri-mun-lung/
https://phongkhamdalieulg.vn/ba-bau-bi-mun-lung/
https://phongkhamdalieulg.vn/nguyen-nhan-gay-mun-lung-o-nu-gioi/
https://phongkhamdalieulg.vn/mun-an-o-lung/
https://phongkhamdalieulg.vn/gynofar-tri-mun-lung/
https://phongkhamdalieulg.vn/nong-gan-noi-mun-o-lung/
https://phongkhamdalieulg.vn/peel-da-mun-lung/
https://phongkhamdalieulg.vn/mun-nhot-o-lung/
https://phongkhamdalieulg.vn/tri-mun-lung-bang-muoi/
https://phongkhamdalieulg.vn/bi-mun-lung-tam-la-gi/
https://phongkhamdalieulg.vn/tri-mun-lung-o-spa-gia-bao-nhieu/
https://phongkhamdalieulg.vn/spa-tri-mun-lung/
https://phongkhamdalieulg.vn/mun-nang-o-lung/
https://phongkhamdalieulg.vn/noi-mun-o-lung-nam-gioi/
https://phongkhamdalieulg.vn/mun-trung-ca-o-lung/
https://phongkhamdalieulg.vn/mun-lung/
https://phongkhamdalieulg.vn/cach-tri-mun-lung-tai-nha/
https://phongkhamdalieulg.vn/cach-tri-mun-lung-tuoi-day-thi/
https://phongkhamdalieulg.vn/cach-tri-mun-lung-trong-1-tuan/
https://phongkhamdalieulg.vn/tri-tham-mun-lung/
https://phongkhamdalieulg.vn/lung-noi-mun-do/
https://phongkhamdalieulg.vn/mun-thit-o-lung/
https://phongkhamdalieulg.vn/cach-tri-mun-o-nguc-va-lung-tai-nha/
https://phongkhamdalieulg.vn/mun-boc-o-lung/
https://phongkhamdalieulg.vn/mun-dau-den-o-lung/
https://phongkhamdalieulg.vn/noi-mun-o-lung-va-vai/
https://phongkhamdalieulg.vn/cach-tri-mun-mu-o-lung/
https://phongkhamdalieulg.vn/tri-mun-o-mat-va-lung/
https://phongkhamdalieulg.vn/bi-mun-o-co-va-lung/
https://phongkhamdalieulg.vn/cach-tri-mun-lung-bang-ca-chua/
https://phongkhamdalieulg.vn/tri-mun-lung-bang-giam-tao/
https://phongkhamdalieulg.vn/tam-kho-qua-tri-mun-lung/
https://phongkhamdalieulg.vn/tri-mun-lung-bang-la-tia-to/
https://phongkhamdalieulg.vn/tri-mun-lung-bang-rau-diep-ca/
https://phongkhamdalieulg.vn/bi-mun-lung-kieng-an-gi/
https://phongkhamdalieulg.vn/kien-thuc-mun-lung-va-viem-nang-long/
"""

# 6. Nhóm VIÊM NANG LÔNG
URL_VIEM_NANG_LONG = """
https://phongkhamdalieulg.vn/viem-nang-long-lung/
https://phongkhamdalieulg.vn/viem-nang-long/
https://phongkhamdalieulg.vn/cach-tri-viem-nang-long/
https://phongkhamdalieulg.vn/viem-lo-chan-long-o-tay/
https://phongkhamdalieulg.vn/viem-nang-long-o-chan/
https://phongkhamdalieulg.vn/viem-nang-long-o-nach/
https://phongkhamdalieulg.vn/viem-nang-long-o-nguc/
https://phongkhamdalieulg.vn/chi-phi-dieu-tri-viem-nang-long/
https://phongkhamdalieulg.vn/viem-nang-long-vung-kin/
https://phongkhamdalieulg.vn/viem-nang-long-o-mat/
https://phongkhamdalieulg.vn/dieu-tri-viem-nang-long-bang-laser/
https://phongkhamdalieulg.vn/viem-nang-long-o-mong/
https://phongkhamdalieulg.vn/viem-nang-long-o-dui/
https://phongkhamdalieulg.vn/cach-tri-viem-lo-chan-long-o-bap-chan/
https://phongkhamdalieulg.vn/viem-lo-chan-long-o-bung/
https://phongkhamdalieulg.vn/viem-nang-long-vung-kin-nam-gioi/
https://phongkhamdalieulg.vn/viem-nang-long-o-co/
https://phongkhamdalieulg.vn/viem-nang-long-co-tu-het-khong/
https://phongkhamdalieulg.vn/viem-nang-long-hau-mon/
https://phongkhamdalieulg.vn/viem-nang-long-hong-ban-hinh-mang-luoi/
https://phongkhamdalieulg.vn/viem-nang-long-co-lay-khong/
https://phongkhamdalieulg.vn/viem-nang-long-co-nen-triet-long-khong/
https://phongkhamdalieulg.vn/lo-chan-long-to-o-chan/
https://phongkhamdalieulg.vn/cao-long-chan-bi-viem-lo-chan-long/
https://phongkhamdalieulg.vn/bi-viem-nang-long-nen-an-gi/
https://phongkhamdalieulg.vn/viem-nang-long-nen-tam-bang-gi/
https://phongkhamdalieulg.vn/bot-dau-do-tri-viem-nang-long/
https://phongkhamdalieulg.vn/mo-tran-co-tri-viem-nang-long-khong/
https://phongkhamdalieulg.vn/tri-viem-lo-chan-long-bang-ba-ca-phe/
https://phongkhamdalieulg.vn/tri-viem-nang-long-bang-dau-dua/
https://phongkhamdalieulg.vn/tri-viem-nang-long-bang-aspirin/
https://phongkhamdalieulg.vn/muoi-tam-tri-viem-nang-long/
https://phongkhamdalieulg.vn/tri-viem-nang-long-bang-la-trau-khong/
https://phongkhamdalieulg.vn/tri-viem-nang-long-bang-nha-dam/
https://phongkhamdalieulg.vn/ba-bau-bi-viem-lo-chan-long/
https://phongkhamdalieulg.vn/ba-bau-bi-viem-nang-long-vung-kin/
https://phongkhamdalieulg.vn/viem-nang-long-sau-khi-wax/
"""

def get_service_name(landing_page):
    # 1. Chuẩn hóa đường dẫn
    path = landing_page.strip()
    full_url = "https://phongkhamdalieulg.vn" + path if path.startswith('/') else path
    
    # 2. ƯU TIÊN SỐ 1: Kiểm tra Trang Chủ trước
    # Điều này ngăn việc "/" bị rơi vào nhóm "Trị Mụn" bên dưới
    if path == "/" or path == "https://phongkhamdalieulg.vn/":
        return "Trang Chủ"
    
    # 3. Kiểm tra các list dịch vụ (Giữ nguyên các biến list của bạn)
    if full_url in URL_TRI_MUN: return "Trị Mụn"
    if full_url in URL_TRI_NAM: return "Trị Nám"
    if full_url in URL_SEO_RO: return "Sẹo Rỗ"
    if full_url in URL_SEO_LOI: return "Sẹo Lồi"
    if full_url in URL_MUN_LUNG: return "Mụn Lưng"
    if full_url in URL_VIEM_NANG_LONG: return "Viêm Nang Lông"
    
    return "Khác"

# =================================================================
# PHẦN XỬ LÝ LOGIC (ĐÃ TỐI ƯU THEO YÊU CẦU)
# =================================================================

# 1. CẤU HÌNH HỆ THỐNG & KẾT NỐI
SCOPES = [
    'https://www.googleapis.com/auth/webmasters.readonly', 
    'https://www.googleapis.com/auth/analytics.readonly'
]

st.set_page_config(page_title="SEO Dashboard - LG Clinic", layout="wide")

# --- HÀM TRỢ GIÚP ---
def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes} phút {secs} giây" if minutes > 0 else f"{secs} giây"

# --- XỬ LÝ XÁC THỰC GOOGLE ---
def get_google_creds():
    CLIENT_ID = st.secrets["google_oauth"]["client_id"]
    CLIENT_SECRET = st.secrets["google_oauth"]["client_secret"]
    REDIRECT_URI = st.secrets["google_oauth"]["redirect_uri"]
    
    AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
    REVOKE_TOKEN_URL = "https://accounts.google.com/o/oauth2/revoke"

    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

    if 'creds' not in st.session_state:
        st.title("🚀 SEO Dashboard - LG Clinic")
        st.info("Vui lòng đăng nhập bằng tài khoản Google quản lý phongkhamdalieulg.vn")
        
        result = oauth2.authorize_button(
            name="🔑 Đăng nhập bằng Google",
            scope=" ".join(SCOPES),
            redirect_uri=REDIRECT_URI,
            key="google_auth",
        )
        
        if result and 'token' in result:
            from google.oauth2.credentials import Credentials
            token_info = result['token']
            st.session_state.creds = Credentials(
                token=token_info.get('access_token'),
                refresh_token=token_info.get('refresh_token'),
                token_uri=TOKEN_URL,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                scopes=SCOPES
            )
            st.rerun()
        st.stop()
    
    return st.session_state.creds

# --- GIAO DIỆN CHÍNH ---
creds = get_google_creds()
gsc_service = build('searchconsole', 'v1', credentials=creds)
ga4_client = BetaAnalyticsDataClient(credentials=creds)

# Sidebar cấu hình
st.sidebar.header("🎯 Cấu hình")
today = datetime.today()
date_range = st.sidebar.date_input("Khoảng thời gian:", [today - timedelta(days=31), today - timedelta(days=1)])
prop_id = st.sidebar.text_input("GA4 Property ID:", "486855373") 
site_url = st.sidebar.text_input("GSC Site URL:", "https://phongkhamdalieulg.vn/")

if len(date_range) == 2 and st.sidebar.button("🚀 Chạy báo cáo"):
    s_str, e_str = date_range[0].strftime('%Y-%m-%d'), date_range[1].strftime('%Y-%m-%d')
    
    with st.spinner("Đang truy xuất dữ liệu từ phongkhamdalieulg.vn..."):
        # 1. TRUY XUẤT GA4
        req_ga4 = RunReportRequest(
            property=f"properties/{prop_id}",
            dimensions=[Dimension(name="landingPagePlusQueryString")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="engagedSessions"),
                Metric(name="engagementRate"),
                Metric(name="userEngagementDuration"),
            ],
            date_ranges=[DateRange(start_date=s_str, end_date=e_str)],
            dimension_filter=FilterExpression(
                filter=Filter(
                    field_name="sessionDefaultChannelGroup",
                    string_filter=Filter.StringFilter(value="Organic Search")
                )
            )
        )
        res_ga = ga4_client.run_report(req_ga4)
        
        ga4_list = []
        if res_ga.rows:
            for row in res_ga.rows:
                full_path = row.dimension_values[0].value
                base_path = full_path.split('?')[0]
                total_sessions = int(row.metric_values[0].value)
                avg_duration = float(row.metric_values[3].value) / total_sessions if total_sessions > 0 else 0
                
                ga4_list.append({
                    'Nhóm Dịch Vụ': get_service_name(base_path), # Áp dụng hàm map URL của bạn
                    'Trang đích': full_path,
                    'Phiên hoạt động': total_sessions,
                    'Số phiên tương tác': int(row.metric_values[1].value),
                    'Tỷ lệ tương tác': f"{float(row.metric_values[2].value)*100:.2f}%",
                    'Thời gian tương tác TB': format_time(avg_duration)
                })
            st.session_state.df_ga4 = pd.DataFrame(ga4_list)

        # 2. TRUY XUẤT GSC & XỬ LÝ TRÙNG LẶP
        res_gsc = gsc_service.searchanalytics().query(siteUrl=site_url, body={
            'startDate': s_str, 'endDate': e_str,
            'dimensions': ['query', 'page'], 'rowLimit': 5000
        }).execute()
        
        if res_gsc.get('rows'):
            df_raw = pd.DataFrame([{
                'Từ khóa': r['keys'][0],
                'Landing Page': r['keys'][1].replace(site_url, "/"),
                'Lượt nhấp': r['clicks'],
                'Lượt hiển thị': r['impressions'],
                'Vị trí TB': r['position']
            } for r in res_gsc['rows']])

            # GOM NHÓM THEO TỪ KHÓA ĐỂ TRÁNH SAI SỐ
            df_gsc_final = df_raw.groupby('Từ khóa').agg({
                'Landing Page': 'first',
                'Lượt nhấp': 'sum',
                'Lượt hiển thị': 'sum',
                'Vị trí TB': 'mean'
            }).reset_index()

            # Áp dụng hàm map URL để phân nhóm dịch vụ
            df_gsc_final['Nhóm Dịch Vụ'] = df_gsc_final['Landing Page'].apply(get_service_name)
            df_gsc_final['Vị trí TB'] = df_gsc_final['Vị trí TB'].round(1)
            
            st.session_state.df_gsc = df_gsc_final.sort_values(by='Lượt nhấp', ascending=False)

# --- HIỂN THỊ DỮ LIỆU ---
if 'df_gsc' in st.session_state and 'df_ga4' in st.session_state:
    df_gsc = st.session_state.df_gsc
    df_ga4 = st.session_state.df_ga4

    st.header("📊 BÁO CÁO HIỆU SUẤT TỔNG QUAN")

    # 1. CÁC CHỈ SỐ KEY METRICS (Nên có cái này đầu tiên)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tổng Lượt Nhấp (GSC)", f"{df_gsc['Lượt nhấp'].sum():,}")
    m2.metric("Tổng Hiển Thị (GSC)", f"{df_gsc['Lượt hiển thị'].sum():,}")
    m3.metric("Tổng Sessions (GA4)", f"{df_ga4['Phiên hoạt động'].sum():,}")
    m4.metric("CTR Trung Bình", f"{(df_gsc['Lượt nhấp'].sum()/df_gsc['Lượt hiển thị'].sum()*100):.2f}%")

    st.markdown("---")

    # 2. BIỂU ĐỒ SO SÁNH DỊCH VỤ
    col1, col2 = st.columns(2)
    
    with col1:
        # Biểu đồ so sánh Nhấp/Hiển thị theo Nhóm Dịch Vụ
        df_service_gsc = df_gsc.groupby('Nhóm Dịch Vụ').agg({'Lượt nhấp': 'sum', 'Lượt hiển thị': 'sum'}).reset_index()
        fig_service = px.bar(df_service_gsc, x='Nhóm Dịch Vụ', y='Lượt nhấp', 
                             text_auto='.2s', title="Hiệu suất Lượt nhấp theo Dịch vụ",
                             color='Lượt nhấp', color_continuous_scale='Blues')
        st.plotly_chart(fig_service, use_container_width=True)

    with col2:
        # Tỉ lệ Traffic GA4
        df_pie_ga4 = df_ga4.groupby('Nhóm Dịch Vụ')['Phiên hoạt động'].sum().reset_index()
        fig_ga4_pie = px.pie(df_pie_ga4, values='Phiên hoạt động', names='Nhóm Dịch Vụ', 
                             title="Tỉ trọng Traffic giữa các Nhóm Dịch Vụ",
                             hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_ga4_pie, use_container_width=True)

    # 3. PHÂN TÍCH CHẤT LƯỢNG NỘI DUNG
    st.subheader("🎯 Top 10 Trang có tương tác tốt nhất (Thời gian ở lại lâu)")
    
    # Xử lý format thời gian để vẽ biểu đồ (chuyển về giây)
    def time_to_seconds(t_str):
        if 'phút' in t_str:
            parts = t_str.split(' phút ')
            return int(parts[0]) * 60 + int(parts[1].replace(' giây', ''))
        return int(t_str.replace(' giây', ''))

    df_ga4_plot = df_ga4.copy()
    df_ga4_plot['Giây tương tác'] = df_ga4_plot['Thời gian tương tác TB'].apply(time_to_seconds)
    df_top_content = df_ga4_plot.sort_values('Giây tương tác', ascending=False).head(10)

    fig_content = px.bar(df_top_content, x='Giây tương tác', y='Trang đích', 
                         orientation='h', color='Nhóm Dịch Vụ',
                         title="Nội dung giữ chân khách hàng lâu nhất (Giây)",
                         labels={'Giây tương tác': 'Giây', 'Trang đích': 'URL'})
    fig_content.update_layout(yaxis={'categoryorder':'total ascending'}) # Sắp xếp cột cao nhất lên đầu
    st.plotly_chart(fig_content, use_container_width=True)

    # 4. BẢNG CHI TIẾT
    st.markdown("---")
    t1, t2 = st.tabs(["🔍 Chi tiết Từ khóa (GSC)", "📈 Chi tiết Trang đích (GA4)"])
    
    with t1:
        st.dataframe(df_gsc, use_container_width=True, hide_index=True)
    with t2:
        st.dataframe(df_ga4, use_container_width=True, hide_index=True)