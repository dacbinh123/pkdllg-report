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

# =================================================================
# PHẦN XỬ LÝ LOGIC (KHÔNG CẦN SỬA DƯỚI NÀY)
# =================================================================

# =================================================================
# 1. CẤU HÌNH HỆ THỐNG & KẾT NỐI
# =================================================================
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

def build_url_mapping():
    mapping = {}
    domain = "https://phongkhamdalieulg.vn"
    # Bạn có thể định nghĩa các URL cụ thể tại đây hoặc lấy từ st.secrets
    groups = {
        "Trị Mụn": "/dich-vu/tri-mun",
        "Trị Nám": "/dich-vu/tri-nam",
        "Sẹo Rỗ": "/dich-vu/tri-seo-ro",
        "Sẹo Lồi": "/dich-vu/tri-seo-loi",
        "Viêm nang lông": "/dich-vu/viem-nang-long",
        "Mụn lưng": "/dich-vu/tri-mun-lung"
    }
    return groups

URL_MAP = build_url_mapping()

# --- XỬ LÝ XÁC THỰC GOOGLE (DÙNG ST.SECRETS) ---
# --- XỬ LÝ XÁC THỰC GOOGLE (DÙNG STREAMLIT-OAUTH) ---
def get_google_creds():
    # 1. Cấu hình các tham số từ Secrets
    CLIENT_ID = st.secrets["google_oauth"]["client_id"]
    CLIENT_SECRET = st.secrets["google_oauth"]["client_secret"]
    REDIRECT_URI = st.secrets["google_oauth"]["redirect_uri"]
    
    AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
    REVOKE_TOKEN_URL = "https://accounts.google.com/o/oauth2/revoke"

    # 2. Khởi tạo component OAuth2
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

    if 'creds' not in st.session_state:
        # Hiển thị tiêu đề và nút đăng nhập cho sếp
        st.title("🚀 SEO Dashboard - LG Clinic")
        st.info("Vui lòng đăng nhập bằng tài khoản Google quản lý phongkhamdalieulg.vn")
        
        # Nút này sẽ tự động mở tab mới và bắt lấy 'code' cho bạn
# Thêm redirect_uri vào trực tiếp nếu cần và bỏ ux_mode nếu không tương thích
        result = oauth2.authorize_button(
            name="🔑 Đăng nhập bằng Google",
            scope=" ".join(SCOPES),
            redirect_uri=REDIRECT_URI, # Đảm bảo tên tham số đúng là redirect_uri
            key="google_auth", # Thêm key để tránh xung đột widget của Streamlit
        )
        
        if result and 'token' in result:
            # Chuyển đổi token nhận được thành đối tượng Credentials của Google
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
                    'Nhóm Dịch Vụ': "Dịch vụ LG Spa", # Bạn có thể map thêm logic phân nhóm tại đây
                    'Trang đích': full_path,
                    'Phiên hoạt động': total_sessions,
                    'Số phiên tương tác': int(row.metric_values[1].value),
                    'Tỷ lệ tương tác': f"{float(row.metric_values[2].value)*100:.2f}%",
                    'Thời gian tương tác TB': format_time(avg_duration)
                })
            st.session_state.df_ga4 = pd.DataFrame(ga4_list)

        # 2. TRUY XUẤT GSC
        res_gsc = gsc_service.searchanalytics().query(siteUrl=site_url, body={
            'startDate': s_str, 'endDate': e_str,
            'dimensions': ['query', 'page'], 'rowLimit': 5000
        }).execute()
        
        if res_gsc.get('rows'):
            df_gsc_new = pd.DataFrame([{
                'Từ khóa': r['keys'][0],
                'Landing Page': r['keys'][1].replace(site_url, "/"),
                'Lượt nhấp': r['clicks'],
                'Lượt hiển thị': r['impressions'],
                'Vị trí TB': round(r['position'], 1)
            } for r in res_gsc['rows']])
            st.session_state.df_gsc = df_gsc_new

# --- HIỂN THỊ DỮ LIỆU ---
if 'df_gsc' in st.session_state and 'df_ga4' in st.session_state:
    df_gsc = st.session_state.df_gsc
    df_ga4 = st.session_state.df_ga4

    st.header("📊 Phân tích Tổng quan")
    col1, col2 = st.columns(2)
    with col1:
        fig_gsc = px.pie(df_gsc.head(10), values='Lượt nhấp', names='Từ khóa', title="Top 10 Từ khóa (Lượt nhấp)")
        st.plotly_chart(fig_gsc, use_container_width=True)
    with col2:
        fig_ga4 = px.pie(df_ga4.head(10), values='Phiên hoạt động', names='Trang đích', title="Top 10 Trang đích (Traffic)")
        st.plotly_chart(fig_ga4, use_container_width=True)

    st.subheader("🔍 Chi tiết Search Console")
    st.dataframe(df_gsc, use_container_width=True, hide_index=True)

    st.subheader("📈 Chi tiết GA4 Organic")
    st.dataframe(df_ga4, use_container_width=True, hide_index=True)