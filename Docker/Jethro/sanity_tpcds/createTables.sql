create table customer_address
(
    ca_address_sk             INTEGER,
    ca_address_id             STRING,
    ca_street_number          STRING,
    ca_street_name            STRING,
    ca_street_type            STRING,
    ca_suite_number           STRING,
    ca_city                   STRING,
    ca_county                 STRING,
    ca_state                  STRING,
    ca_zip                    STRING,
    ca_country                STRING,
    ca_gmt_offset             FLOAT,
    ca_location_type          STRING
);
create table customer_demographics
(
    cd_demo_sk                INTEGER,
    cd_gender                 STRING,
    cd_marital_status         STRING,
    cd_education_status       STRING,
    cd_purchase_estimate      INTEGER,
    cd_credit_rating          STRING,
    cd_dep_count              INTEGER,
    cd_dep_employed_count     INTEGER,
    cd_dep_college_count      INTEGER
);
create table date_dim
(
    d_date_sk                 INTEGER,
    d_date_id                 STRING,
    d_date                    TIMESTAMP,
    d_month_seq               INTEGER,
    d_week_seq                INTEGER,
    d_quarter_seq             INTEGER,
    d_year                    INTEGER,
    d_dow                     INTEGER,
    d_moy                     INTEGER,
    d_dom                     INTEGER,
    d_qoy                     INTEGER,
    d_fy_year                 INTEGER,
    d_fy_quarter_seq          INTEGER,
    d_fy_week_seq             INTEGER,
    d_day_name                STRING,
    d_quarter_name            STRING,
    d_holiday                 STRING,
    d_weekend                 STRING,
    d_following_holiday       STRING,
    d_first_dom               INTEGER,
    d_last_dom                INTEGER,
    d_same_day_ly             INTEGER,
    d_same_day_lq             INTEGER,
    d_current_day             STRING,
    d_current_week            STRING,
    d_current_month           STRING,
    d_current_quarter         STRING,
    d_current_year            STRING
);
create table warehouse
(
    w_warehouse_sk            INTEGER,
    w_warehouse_id            STRING,
    w_warehouse_name          STRING,
    w_warehouse_sq_ft         INTEGER,
    w_street_number           STRING,
    w_street_name             STRING,
    w_street_type             STRING,
    w_suite_number            STRING,
    w_city                    STRING,
    w_county                  STRING,
    w_state                   STRING,
    w_zip                     STRING,
    w_country                 STRING,
    w_gmt_offset              FLOAT
);
create table ship_mode
(
    sm_ship_mode_sk           INTEGER,
    sm_ship_mode_id           STRING,
    sm_type                   STRING,
    sm_code                   STRING,
    sm_carrier                STRING,
    sm_contract               STRING
);
create table time_dim
(
    t_time_sk                 INTEGER,
    t_time_id                 STRING,
    t_time                    INTEGER,
    t_hour                    INTEGER,
    t_minute                  INTEGER,
    t_second                  INTEGER,
    t_am_pm                   STRING,
    t_shift                   STRING,
    t_sub_shift               STRING,
    t_meal_time               STRING
);
create table reason
(
    r_reason_sk               INTEGER,
    r_reason_id               STRING,
    r_reason_desc             STRING
);
create table income_band
(
    ib_income_band_sk         INTEGER,
    ib_lower_bound            INTEGER,
    ib_upper_bound            INTEGER
);
create table item
(
    i_item_sk                 INTEGER,
    i_item_id                 STRING,
    i_rec_start_date          TIMESTAMP,
    i_rec_end_date            TIMESTAMP,
    i_item_desc               STRING,
    i_current_price           DOUBLE,
    i_wholesale_cost          DOUBLE,
    i_brand_id                INTEGER,
    i_brand                   STRING,
    i_class_id                INTEGER,
    i_class                   STRING,
    i_category_id             INTEGER,
    i_category                STRING,
    i_manufact_id             INTEGER,
    i_manufact                STRING,
    i_size                    STRING,
    i_formulation             STRING,
    i_color                   STRING,
    i_units                   STRING,
    i_container               STRING,
    i_manager_id              INTEGER,
    i_product_name            STRING
);
create table store
(
    s_store_sk                INTEGER,
    s_store_id                STRING,
    s_rec_start_date          TIMESTAMP,
    s_rec_end_date            TIMESTAMP,
    s_closed_date_sk          INTEGER,
    s_store_name              STRING,
    s_number_employees        INTEGER,
    s_floor_space             INTEGER,
    s_hours                   STRING,
    s_manager                 STRING,
    s_market_id               INTEGER,
    s_geography_class         STRING,
    s_market_desc             STRING,
    s_market_manager          STRING,
    s_division_id             INTEGER,
    s_division_name           STRING,
    s_company_id              INTEGER,
    s_company_name            STRING,
    s_street_number           STRING,
    s_street_name             STRING,
    s_street_type             STRING,
    s_suite_number            STRING,
    s_city                    STRING,
    s_county                  STRING,
    s_state                   STRING,
    s_zip                     STRING,
    s_country                 STRING,
    s_gmt_offset              FLOAT,
    s_tax_precentage          FLOAT
);
create table call_center
(
    cc_call_center_sk         INTEGER,
    cc_call_center_id         STRING,
    cc_rec_start_date         TIMESTAMP,
    cc_rec_end_date           TIMESTAMP,
    cc_closed_date_sk         INTEGER,
    cc_open_date_sk           INTEGER,
    cc_name                   STRING,
    cc_class                  STRING,
    cc_employees              INTEGER,
    cc_sq_ft                  INTEGER,
    cc_hours                  STRING,
    cc_manager                STRING,
    cc_mkt_id                 INTEGER,
    cc_mkt_class              STRING,
    cc_mkt_desc               STRING,
    cc_market_manager         STRING,
    cc_division               INTEGER,
    cc_division_name          STRING,
    cc_company                INTEGER,
    cc_company_name           STRING,
    cc_street_number          STRING,
    cc_street_name            STRING,
    cc_street_type            STRING,
    cc_suite_number           STRING,
    cc_city                   STRING,
    cc_county                 STRING,
    cc_state                  STRING,
    cc_zip                    STRING,
    cc_country                STRING,
    cc_gmt_offset             FLOAT,
    cc_tax_percentage         DOUBLE
);
create table customer
(
    c_customer_sk             INTEGER,
    c_customer_id             STRING,
    c_current_cdemo_sk        INTEGER,
    c_current_hdemo_sk        INTEGER,
    c_current_addr_sk         INTEGER,
    c_first_shipto_date_sk    INTEGER,
    c_first_sales_date_sk     INTEGER,
    c_salutation              STRING,
    c_first_name              STRING,
    c_last_name               STRING,
    c_preferred_cust_flag     STRING,
    c_birth_day               INTEGER,
    c_birth_month             INTEGER,
    c_birth_year              INTEGER,
    c_birth_country           STRING,
    c_login                   STRING,
    c_email_address           STRING,
    c_last_review_date        STRING
);
create table web_site
(
    web_site_sk               INTEGER,
    web_site_id               STRING,
    web_rec_start_date        TIMESTAMP,
    web_rec_end_date          TIMESTAMP,
    web_name                  STRING,
    web_open_date_sk          INTEGER,
    web_close_date_sk         INTEGER,
    web_class                 STRING,
    web_manager               STRING,
    web_mkt_id                INTEGER,
    web_mkt_class             STRING,
    web_mkt_desc              STRING,
    web_market_manager        STRING,
    web_company_id            INTEGER,
    web_company_name          STRING,
    web_street_number         STRING,
    web_street_name           STRING,
    web_street_type           STRING,
    web_suite_number          STRING,
    web_city                  STRING,
    web_county                STRING,
    web_state                 STRING,
    web_zip                   STRING,
    web_country               STRING,
    web_gmt_offset            FLOAT,
    web_tax_percentage        DOUBLE
);
create table store_returns
(
    sr_returned_date_sk       INTEGER,
    sr_return_time_sk         INTEGER,
    sr_item_sk                INTEGER,
    sr_customer_sk            INTEGER,
    sr_cdemo_sk               INTEGER,
    sr_hdemo_sk               INTEGER,
    sr_addr_sk                INTEGER,
    sr_store_sk               INTEGER,
    sr_reason_sk              INTEGER,
    sr_ticket_number          INTEGER,
    sr_return_quantity        INTEGER,
    sr_return_amt             DOUBLE,
    sr_return_tax             DOUBLE,
    sr_return_amt_inc_tax     DOUBLE,
    sr_fee                    FLOAT,
    sr_return_ship_cost       FLOAT,
    sr_refunded_cash          FLOAT,
    sr_reversed_charge        DOUBLE,
    sr_store_credit           DOUBLE,
    sr_net_loss               DOUBLE
);
create table household_demographics
(
    hd_demo_sk                INTEGER,
    hd_income_band_sk         INTEGER,
    hd_buy_potential          STRING,
    hd_dep_count              INTEGER,
    hd_vehicle_count          INTEGER
);
create table web_page
(
    wp_web_page_sk            INTEGER,
    wp_web_page_id            STRING,
    wp_rec_start_date         TIMESTAMP,
    wp_rec_end_date           TIMESTAMP,
    wp_creation_date_sk       INTEGER,
    wp_access_date_sk         INTEGER,
    wp_autogen_flag           STRING,
    wp_customer_sk            INTEGER,
    wp_url                    STRING,
    wp_type                   STRING,
    wp_char_count             INTEGER,
    wp_link_count             INTEGER,
    wp_image_count            INTEGER,
    wp_max_ad_count           INTEGER
);
create table promotion
(
    p_promo_sk                INTEGER,
    p_promo_id                STRING,
    p_start_date_sk           INTEGER,
    p_end_date_sk             INTEGER,
    p_item_sk                 INTEGER,
    p_cost                    DOUBLE,
    p_response_target         INTEGER,
    p_promo_name              STRING,
    p_channel_dmail           STRING,
    p_channel_email           STRING,
    p_channel_catalog         STRING,
    p_channel_tv              STRING,
    p_channel_radio           STRING,
    p_channel_press           STRING,
    p_channel_event           STRING,
    p_channel_demo            STRING,
    p_channel_details         STRING,
    p_purpose                 STRING,
    p_discount_active         STRING
);
create table catalog_page
(
    cp_catalog_page_sk        INTEGER,
    cp_catalog_page_id        STRING,
    cp_start_date_sk          INTEGER,
    cp_end_date_sk            INTEGER,
    cp_department             STRING,
    cp_catalog_number         INTEGER,
    cp_catalog_page_number    INTEGER,
    cp_description            STRING,
    cp_type                   STRING
);
create table inventory
(
    inv_date_sk               INTEGER,
    inv_item_sk               INTEGER,
    inv_warehouse_sk          INTEGER,
    inv_quantity_on_hand      INTEGER
);
create table catalog_returns
(
    cr_returned_date_sk       INTEGER,
    cr_returned_time_sk       INTEGER,
    cr_item_sk                INTEGER,
    cr_refunded_customer_sk   INTEGER,
    cr_refunded_cdemo_sk      INTEGER,
    cr_refunded_hdemo_sk      INTEGER,
    cr_refunded_addr_sk       INTEGER,
    cr_returning_customer_sk  INTEGER,
    cr_returning_cdemo_sk     INTEGER,
    cr_returning_hdemo_sk     INTEGER,
    cr_returning_addr_sk      INTEGER,
    cr_call_center_sk         INTEGER,
    cr_catalog_page_sk        INTEGER,
    cr_ship_mode_sk           INTEGER,
    cr_warehouse_sk           INTEGER,
    cr_reason_sk              INTEGER,
    cr_order_number           INTEGER,
    cr_return_quantity        INTEGER,
    cr_return_amount          DOUBLE,
    cr_return_tax             DOUBLE,
    cr_return_amt_inc_tax     DOUBLE,
    cr_fee                    DOUBLE,
    cr_return_ship_cost       FLOAT,
    cr_refunded_cash          FLOAT,
    cr_reversed_charge        FLOAT,
    cr_store_credit           FLOAT,
    cr_net_loss               DOUBLE
);
create table web_returns
(
    wr_returned_date_sk       INTEGER,
    wr_returned_time_sk       INTEGER,
    wr_item_sk                INTEGER,
    wr_refunded_customer_sk   INTEGER,
    wr_refunded_cdemo_sk      INTEGER,
    wr_refunded_hdemo_sk      INTEGER,
    wr_refunded_addr_sk       INTEGER,
    wr_returning_customer_sk  INTEGER,
    wr_returning_cdemo_sk     INTEGER,
    wr_returning_hdemo_sk     INTEGER,
    wr_returning_addr_sk      INTEGER,
    wr_web_page_sk            INTEGER,
    wr_reason_sk              INTEGER,
    wr_order_number           INTEGER,
    wr_return_quantity        INTEGER,
    wr_return_amt             DOUBLE,
    wr_return_tax             FLOAT,
    wr_return_amt_inc_tax     DOUBLE,
    wr_fee                    FLOAT,
    wr_return_ship_cost       DOUBLE,
    wr_refunded_cash          DOUBLE,
    wr_reversed_charge        DOUBLE,
    wr_account_credit         FLOAT,
    wr_net_loss               FLOAT
);
create table web_sales
(
    ws_sold_date_sk           BIGINT,
    ws_sold_time_sk           BIGINT,
    ws_ship_date_sk           BIGINT,
    ws_item_sk                BIGINT,
    ws_bill_customer_sk       BIGINT,
    ws_bill_cdemo_sk          INTEGER,
    ws_bill_hdemo_sk          INTEGER,
    ws_bill_addr_sk           INTEGER,
    ws_ship_customer_sk       INTEGER,
    ws_ship_cdemo_sk          INTEGER,
    ws_ship_hdemo_sk          INTEGER,
    ws_ship_addr_sk           INTEGER,
    ws_web_page_sk            INTEGER,
    ws_web_site_sk            INTEGER,
    ws_ship_mode_sk           INTEGER,
    ws_warehouse_sk           INTEGER,
    ws_promo_sk               INTEGER,
    ws_order_number           INTEGER,
    ws_quantity               INTEGER,
    ws_wholesale_cost         DOUBLE,
    ws_list_price             DOUBLE,
    ws_sales_price            DOUBLE,
    ws_ext_discount_amt       DOUBLE,
    ws_ext_sales_price        FLOAT,
    ws_ext_wholesale_cost     DOUBLE,
    ws_ext_list_price         DOUBLE,
    ws_ext_tax                FLOAT,
    ws_coupon_amt             FLOAT,
    ws_ext_ship_cost          FLOAT,
    ws_net_paid               DOUBLE,
    ws_net_paid_inc_tax       FLOAT,
    ws_net_paid_inc_ship      FLOAT,
    ws_net_paid_inc_ship_tax  DOUBLE,
    ws_net_profit             DOUBLE
);
create table catalog_sales
(
    cs_sold_date_sk           INTEGER,
    cs_sold_time_sk           INTEGER,
    cs_ship_date_sk           INTEGER,
    cs_bill_customer_sk       INTEGER,
    cs_bill_cdemo_sk          INTEGER,
    cs_bill_hdemo_sk          INTEGER,
    cs_bill_addr_sk           INTEGER,
    cs_ship_customer_sk       INTEGER,
    cs_ship_cdemo_sk          INTEGER,
    cs_ship_hdemo_sk          INTEGER,
    cs_ship_addr_sk           INTEGER,
    cs_call_center_sk         INTEGER,
    cs_catalog_page_sk        INTEGER,
    cs_ship_mode_sk           INTEGER,
    cs_warehouse_sk           INTEGER,
    cs_item_sk                INTEGER,
    cs_promo_sk               INTEGER,
    cs_order_number           INTEGER,
    cs_quantity               INTEGER,
    cs_wholesale_cost         DOUBLE,
    cs_list_price             DOUBLE,
    cs_sales_price            DOUBLE,
    cs_ext_discount_amt       DOUBLE,
    cs_ext_sales_price        FLOAT,
    cs_ext_wholesale_cost     FLOAT,
    cs_ext_list_price         FLOAT,
    cs_ext_tax                FLOAT,
    cs_coupon_amt             FLOAT,
    cs_ext_ship_cost          FLOAT,
    cs_net_paid               FLOAT,
    cs_net_paid_inc_tax       DOUBLE,
    cs_net_paid_inc_ship      DOUBLE,
    cs_net_paid_inc_ship_tax  DOUBLE,
    cs_net_profit             DOUBLE
);
create table store_sales
(
    ss_sold_date_sk           INTEGER,
    ss_sold_time_sk           INTEGER,
    ss_item_sk                INTEGER,
    ss_customer_sk            INTEGER,
    ss_cdemo_sk               INTEGER,
    ss_hdemo_sk               INTEGER,
    ss_addr_sk                INTEGER,
    ss_store_sk               INTEGER,
    ss_promo_sk               INTEGER,
    ss_ticket_number          INTEGER,
    ss_quantity               INTEGER,
    ss_wholesale_cost         FLOAT,
    ss_list_price             FLOAT,
    ss_sales_price            FLOAT,
    ss_ext_discount_amt       FLOAT,
    ss_ext_sales_price        FLOAT,
    ss_ext_wholesale_cost     FLOAT,
    ss_ext_list_price         DOUBLE,
    ss_ext_tax                DOUBLE,
    ss_coupon_amt             DOUBLE,
    ss_net_paid               DOUBLE,
    ss_net_paid_inc_tax       DOUBLE,
    ss_net_profit             DOUBLE
) PARTITION BY RANGE (ss_sold_date_sk) EVERY(30);