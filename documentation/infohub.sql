create schema public
grant usage on schema public to public;
grant create on schema public to public;

create table if not exists users_customuser
(
    id           serial                   not null
        constraint users_customuser_pkey
            primary key,
    password     varchar(128)             not null,
    last_login   timestamp with time zone,
    is_superuser boolean                  not null,
    username     varchar(150)             not null
        constraint users_customuser_username_key
            unique,
    first_name   varchar(30)              not null,
    last_name    varchar(150)             not null,
    is_staff     boolean                  not null,
    is_active    boolean                  not null,
    date_joined  timestamp with time zone not null,
    email        varchar(25)              not null
        constraint users_customuser_email_key
            unique
);

alter table users_customuser
    owner to kent;

create index if not exists users_customuser_username_80452fdf_like
    on users_customuser (username);

create index if not exists users_customuser_email_6445acef_like
    on users_customuser (email);

create table if not exists users_customuser_groups
(
    id            serial  not null
        constraint users_customuser_groups_pkey
            primary key,
    customuser_id integer not null
        constraint users_customuser_gro_customuser_id_958147bf_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    group_id      integer not null,
    constraint users_customuser_groups_customuser_id_group_id_76b619e3_uniq
        unique (customuser_id, group_id)
);

alter table users_customuser_groups
    owner to kent;

create index if not exists users_customuser_groups_customuser_id_958147bf
    on users_customuser_groups (customuser_id);

create index if not exists users_customuser_groups_group_id_01390b14
    on users_customuser_groups (group_id);

create table if not exists users_customuser_user_permissions
(
    id            serial  not null
        constraint users_customuser_user_permissions_pkey
            primary key,
    customuser_id integer not null
        constraint users_customuser_use_customuser_id_5771478b_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    permission_id integer not null,
    constraint users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq
        unique (customuser_id, permission_id)
);

alter table users_customuser_user_permissions
    owner to kent;

create index if not exists users_customuser_user_permissions_customuser_id_5771478b
    on users_customuser_user_permissions (customuser_id);

create index if not exists users_customuser_user_permissions_permission_id_baaa2f74
    on users_customuser_user_permissions (permission_id);

create table if not exists users_team
(
    team_id                 serial                   not null
        constraint users_team_pkey
            primary key,
    team_code               varchar(20)              not null
        constraint users_team_team_code_key
            unique,
    team_name               varchar(50)              not null
        constraint users_team_team_name_key
            unique,
    team_desc               varchar(150)             not null,
    team_date_created       timestamp with time zone not null,
    team_date_updated       timestamp with time zone,
    team_date_created_by_id integer
        constraint users_team_team_date_created_by_cc218cc0_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    team_date_updated_by_id integer
        constraint users_team_team_date_updated_by_4b18f586_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    team_lead_id            integer                  not null
        constraint users_team_team_lead_id_547d78d9_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred
);

alter table users_team
    owner to kent;

create index if not exists users_team_team_code_a1fce7f2_like
    on users_team (team_code);

create index if not exists users_team_team_name_1a43a920_like
    on users_team (team_name);

create index if not exists users_team_team_date_created_by_id_cc218cc0
    on users_team (team_date_created_by_id);

create index if not exists users_team_team_date_updated_by_id_4b18f586
    on users_team (team_date_updated_by_id);

create index if not exists users_team_team_lead_id_547d78d9
    on users_team (team_lead_id);

create table if not exists users_profile
(
    id                serial       not null
        constraint users_profile_pkey
            primary key,
    user_code         varchar(30)  not null,
    middle_name       varchar(30)  not null,
    extension_name    varchar(5)   not null,
    nickname          varchar(25)  not null,
    marital_status    smallint     not null
        constraint users_profile_marital_status_check
            check (marital_status >= 0),
    phone_number      varchar(25)  not null,
    mobile_number     varchar(25)  not null,
    birth_date        date,
    present_address   text         not null,
    permanent_address text         not null,
    gender            smallint     not null
        constraint users_profile_gender_check
            check (gender >= 0),
    image             varchar(100) not null,
    type              smallint     not null
        constraint users_profile_type_check
            check (type >= 0),
    team_id           integer
        constraint users_profile_team_id_14b6fa44_fk_users_team_team_id
            references users_team
            deferrable initially deferred,
    user_id           integer      not null
        constraint users_profile_user_id_key
            unique
        constraint users_profile_user_id_2112e78d_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred
);

alter table users_profile
    owner to kent;

create index if not exists users_profile_team_id_14b6fa44
    on users_profile (team_id);

create table if not exists account_emailaddress
(
    id        serial       not null
        constraint account_emailaddress_pkey
            primary key,
    email     varchar(254) not null
        constraint account_emailaddress_email_key
            unique,
    verified  boolean      not null,
    "primary" boolean      not null,
    user_id   integer      not null
        constraint account_emailaddress_user_id_2c513194_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred
);

alter table account_emailaddress
    owner to kent;

create index if not exists account_emailaddress_user_id_2c513194
    on account_emailaddress (user_id);

create index if not exists account_emailaddress_email_03be32b2_like
    on account_emailaddress (email);

create table if not exists account_emailconfirmation
(
    id               serial                   not null
        constraint account_emailconfirmation_pkey
            primary key,
    created          timestamp with time zone not null,
    sent             timestamp with time zone,
    key              varchar(64)              not null
        constraint account_emailconfirmation_key_key
            unique,
    email_address_id integer                  not null
        constraint account_emailconfirm_email_address_id_5b7f8c58_fk_account_e
            references account_emailaddress
            deferrable initially deferred
);

alter table account_emailconfirmation
    owner to kent;

create index if not exists account_emailconfirmation_key_f43612bd_like
    on account_emailconfirmation (key);

create index if not exists account_emailconfirmation_email_address_id_5b7f8c58
    on account_emailconfirmation (email_address_id);

create table if not exists django_session
(
    session_key  varchar(40)              not null
        constraint django_session_pkey
            primary key,
    session_data text                     not null,
    expire_date  timestamp with time zone not null
);

alter table django_session
    owner to kent;

create index if not exists django_session_session_key_c0390e0f_like
    on django_session (session_key);

create index if not exists django_session_expire_date_a5c62663
    on django_session (expire_date);

create table if not exists django_site
(
    id     serial       not null
        constraint django_site_pkey
            primary key,
    domain varchar(100) not null
        constraint django_site_domain_a2e37b91_uniq
            unique,
    name   varchar(50)  not null
);

alter table django_site
    owner to kent;

create index if not exists django_site_domain_a2e37b91_like
    on django_site (domain);

create table if not exists socialaccount_socialaccount
(
    id          serial                   not null
        constraint socialaccount_socialaccount_pkey
            primary key,
    provider    varchar(30)              not null,
    uid         varchar(191)             not null,
    last_login  timestamp with time zone not null,
    date_joined timestamp with time zone not null,
    extra_data  text                     not null,
    user_id     integer                  not null
        constraint socialaccount_social_user_id_8146e70c_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    constraint socialaccount_socialaccount_provider_uid_fc810c6e_uniq
        unique (provider, uid)
);

alter table socialaccount_socialaccount
    owner to kent;

create index if not exists socialaccount_socialaccount_user_id_8146e70c
    on socialaccount_socialaccount (user_id);

create table if not exists socialaccount_socialapp
(
    id        serial       not null
        constraint socialaccount_socialapp_pkey
            primary key,
    provider  varchar(30)  not null,
    name      varchar(40)  not null,
    client_id varchar(191) not null,
    secret    varchar(191) not null,
    key       varchar(191) not null
);

alter table socialaccount_socialapp
    owner to kent;

create table if not exists socialaccount_socialapp_sites
(
    id           serial  not null
        constraint socialaccount_socialapp_sites_pkey
            primary key,
    socialapp_id integer not null
        constraint socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc
            references socialaccount_socialapp
            deferrable initially deferred,
    site_id      integer not null
        constraint socialaccount_social_site_id_2579dee5_fk_django_si
            references django_site
            deferrable initially deferred,
    constraint socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq
        unique (socialapp_id, site_id)
);

alter table socialaccount_socialapp_sites
    owner to kent;

create index if not exists socialaccount_socialapp_sites_socialapp_id_97fb6e7d
    on socialaccount_socialapp_sites (socialapp_id);

create index if not exists socialaccount_socialapp_sites_site_id_2579dee5
    on socialaccount_socialapp_sites (site_id);

create table if not exists socialaccount_socialtoken
(
    id           serial  not null
        constraint socialaccount_socialtoken_pkey
            primary key,
    token        text    not null,
    token_secret text    not null,
    expires_at   timestamp with time zone,
    account_id   integer not null
        constraint socialaccount_social_account_id_951f210e_fk_socialacc
            references socialaccount_socialaccount
            deferrable initially deferred,
    app_id       integer not null
        constraint socialaccount_social_app_id_636a42d7_fk_socialacc
            references socialaccount_socialapp
            deferrable initially deferred,
    constraint socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq
        unique (app_id, account_id)
);

alter table socialaccount_socialtoken
    owner to kent;

create index if not exists socialaccount_socialtoken_account_id_951f210e
    on socialaccount_socialtoken (account_id);

create index if not exists socialaccount_socialtoken_app_id_636a42d7
    on socialaccount_socialtoken (app_id);

create table if not exists tickets_comment
(
    comment_id          serial                   not null
        constraint tickets_comment_pkey
            primary key,
    comment_description text                     not null,
    comment_date_added  timestamp with time zone not null,
    comment_user_id     integer                  not null
        constraint tickets_comment_comment_user_id_6a0f2eaa_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    ticket_id           integer                  not null
);

alter table tickets_comment
    owner to kent;

create index if not exists tickets_comment_comment_user_id_6a0f2eaa
    on tickets_comment (comment_user_id);

create index if not exists tickets_comment_ticket_id_36a9497d
    on tickets_comment (ticket_id);

create table if not exists tickets_status
(
    stat_id          serial                   not null
        constraint tickets_status_pkey
            primary key,
    stat_code        varchar(20)              not null,
    stat_name        varchar(25)              not null,
    stat_description varchar(250)             not null,
    stat_last_update timestamp with time zone not null,
    stat_date_added  timestamp with time zone not null,
    stat_author_id   integer                  not null
        constraint tickets_status_stat_author_id_7c25c4b0_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred
);

alter table tickets_status
    owner to kent;

create table if not exists tickets_category
(
    cat_id          serial                   not null
        constraint tickets_category_pkey
            primary key,
    cat_code        varchar(20)              not null,
    cat_name        varchar(25)              not null,
    cat_description varchar(45)              not null,
    cat_last_update timestamp with time zone not null,
    cat_date_added  timestamp with time zone not null,
    cat_author_id   integer                  not null
        constraint tickets_category_cat_author_id_47c148a3_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    cat_status_id   integer                  not null
        constraint tickets_category_cat_status_id_79cc31f4_fk_tickets_s
            references tickets_status
            deferrable initially deferred
);

alter table tickets_category
    owner to kent;

create index if not exists tickets_category_cat_author_id_47c148a3
    on tickets_category (cat_author_id);

create index if not exists tickets_category_cat_status_id_79cc31f4
    on tickets_category (cat_status_id);

create table if not exists tickets_client
(
    client_id                serial                   not null
        constraint tickets_client_pkey
            primary key,
    client_code              varchar(20)              not null,
    client_name              varchar(50)              not null,
    client_address           varchar(100)             not null,
    client_last_update       timestamp with time zone not null,
    client_date_added        timestamp with time zone not null,
    account_manager_id       integer                  not null
        constraint tickets_client_account_manager_id_2044cffa_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    client_author_id         integer                  not null
        constraint tickets_client_client_author_id_15ed9cb6_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    client_status_id         integer                  not null
        constraint tickets_client_client_status_id_61d143b2_fk_tickets_s
            references tickets_status
            deferrable initially deferred,
    client_last_update_by_id integer
        constraint tickets_client_client_last_update_b_9a2e32ae_fk_users_cus
            references users_customuser
            deferrable initially deferred
);

alter table tickets_client
    owner to kent;

create index if not exists tickets_client_account_manager_id_2044cffa
    on tickets_client (account_manager_id);

create index if not exists tickets_client_client_author_id_15ed9cb6
    on tickets_client (client_author_id);

create index if not exists tickets_client_client_status_id_61d143b2
    on tickets_client (client_status_id);

create index if not exists tickets_client_client_last_update_by_id_9a2e32ae
    on tickets_client (client_last_update_by_id);

create table if not exists tickets_product
(
    prod_id          serial                   not null
        constraint tickets_product_pkey
            primary key,
    prod_code        varchar(20)              not null,
    prod_name        varchar(25)              not null,
    prod_description varchar(250)             not null,
    prod_type_id     integer                  not null,
    prod_last_update timestamp with time zone not null,
    prod_date_added  timestamp with time zone not null,
    client_id        integer                  not null
        constraint tickets_product_client_id_a00667e3_fk_tickets_client_client_id
            references tickets_client
            deferrable initially deferred,
    prod_author_id   integer                  not null
        constraint tickets_product_prod_author_id_1109cfed_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    prod_manager_id  integer                  not null
        constraint tickets_product_prod_manager_id_9a27c86d_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    prod_status_id   integer                  not null
        constraint tickets_product_prod_status_id_62862b07_fk_tickets_s
            references tickets_status
            deferrable initially deferred
);

alter table tickets_product
    owner to kent;

create table if not exists tickets_module
(
    mod_id          serial                   not null
        constraint tickets_module_pkey
            primary key,
    mod_code        varchar(20)              not null,
    mod_name        varchar(25)              not null,
    mod_description varchar(45)              not null,
    mod_last_update timestamp with time zone not null,
    mod_date_added  timestamp with time zone not null,
    mod_author_id   integer                  not null
        constraint tickets_module_mod_author_id_f9a79442_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    mod_status_id   integer                  not null
        constraint tickets_module_mod_status_id_ddf88325_fk_tickets_status_stat_id
            references tickets_status
            deferrable initially deferred,
    product_id      integer                  not null
        constraint tickets_module_product_id_2be4c338_fk_tickets_product_prod_id
            references tickets_product
            deferrable initially deferred
);

alter table tickets_module
    owner to kent;

create table if not exists tickets_hotissue
(
    hi_id                serial                   not null
        constraint tickets_hotissue_pkey
            primary key,
    hi_code              varchar(20)              not null,
    hi_name              varchar(25)              not null,
    hi_description       varchar(45)              not null,
    hi_last_update       timestamp with time zone not null,
    hi_date_added        timestamp with time zone not null,
    hi_date_closed       timestamp with time zone not null,
    hi_author_id         integer                  not null
        constraint tickets_hotissue_hi_author_id_7fba5c97_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    hi_last_update_by_id integer
        constraint tickets_hotissue_hi_last_update_by_id_5498f355_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    hi_module_id         integer
        constraint tickets_hotissue_hi_module_id_68e77bc3_fk_tickets_module_mod_id
            references tickets_module
            deferrable initially deferred,
    hi_product_id        integer                  not null
        constraint tickets_hotissue_hi_product_id_3db04b33_fk_tickets_p
            references tickets_product
            deferrable initially deferred,
    hi_status_id         integer                  not null
        constraint tickets_hotissue_hi_status_id_9f9d9a1a_fk_tickets_s
            references tickets_status
            deferrable initially deferred
);

alter table tickets_hotissue
    owner to kent;

create index if not exists tickets_hotissue_hi_author_id_7fba5c97
    on tickets_hotissue (hi_author_id);

create index if not exists tickets_hotissue_hi_last_update_by_id_5498f355
    on tickets_hotissue (hi_last_update_by_id);

create index if not exists tickets_hotissue_hi_module_id_68e77bc3
    on tickets_hotissue (hi_module_id);

create index if not exists tickets_hotissue_hi_product_id_3db04b33
    on tickets_hotissue (hi_product_id);

create index if not exists tickets_hotissue_hi_status_id_9f9d9a1a
    on tickets_hotissue (hi_status_id);

create index if not exists tickets_module_mod_author_id_f9a79442
    on tickets_module (mod_author_id);

create index if not exists tickets_module_mod_status_id_ddf88325
    on tickets_module (mod_status_id);

create index if not exists tickets_module_product_id_2be4c338
    on tickets_module (product_id);

create index if not exists tickets_product_client_id_a00667e3
    on tickets_product (client_id);

create index if not exists tickets_product_prod_author_id_1109cfed
    on tickets_product (prod_author_id);

create index if not exists tickets_product_prod_manager_id_9a27c86d
    on tickets_product (prod_manager_id);

create index if not exists tickets_product_prod_status_id_62862b07
    on tickets_product (prod_status_id);

create table if not exists tickets_project
(
    proj_id                serial                   not null
        constraint tickets_project_pkey
            primary key,
    proj_code              varchar(20)              not null,
    proj_name              varchar(25)              not null,
    proj_description       varchar(250)             not null,
    proj_complete_date     timestamp with time zone,
    proj_warranty_end      date,
    proj_last_update       timestamp with time zone,
    proj_date_added        timestamp with time zone not null,
    proj_author_id         integer                  not null
        constraint tickets_project_proj_author_id_7c4e89d0_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    proj_client_id         integer                  not null
        constraint tickets_project_proj_client_id_cd0470b8_fk_tickets_c
            references tickets_client
            deferrable initially deferred,
    proj_manager_id        integer                  not null
        constraint tickets_project_proj_manager_id_e2769405_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    proj_status_id         integer                  not null
        constraint tickets_project_proj_status_id_f682194c_fk_tickets_s
            references tickets_status
            deferrable initially deferred,
    proj_last_update_by_id integer
        constraint tickets_project_proj_last_update_by__f555be91_fk_users_cus
            references users_customuser
            deferrable initially deferred
);

alter table tickets_project
    owner to kent;

create index if not exists tickets_project_proj_author_id_7c4e89d0
    on tickets_project (proj_author_id);

create index if not exists tickets_project_proj_client_id_cd0470b8
    on tickets_project (proj_client_id);

create index if not exists tickets_project_proj_manager_id_e2769405
    on tickets_project (proj_manager_id);

create index if not exists tickets_project_proj_status_id_f682194c
    on tickets_project (proj_status_id);

create index if not exists tickets_project_proj_last_update_by_id_f555be91
    on tickets_project (proj_last_update_by_id);

create index if not exists tickets_status_stat_author_id_7c25c4b0
    on tickets_status (stat_author_id);

create table if not exists tickets_subcategory
(
    scat_id          serial                   not null
        constraint tickets_subcategory_pkey
            primary key,
    scat_code        varchar(20)              not null,
    scat_name        varchar(25)              not null,
    scat_description varchar(45)              not null,
    scat_last_update timestamp with time zone not null,
    scat_date_added  timestamp with time zone not null,
    category_id      integer                  not null
        constraint tickets_subcategory_category_id_c2586920_fk_tickets_c
            references tickets_category
            deferrable initially deferred,
    scat_author_id   integer                  not null
        constraint tickets_subcategory_scat_author_id_0acaf9ac_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    scat_status_id   integer                  not null
        constraint tickets_subcategory_scat_status_id_c8b91926_fk_tickets_s
            references tickets_status
            deferrable initially deferred
);

alter table tickets_subcategory
    owner to kent;

create index if not exists tickets_subcategory_category_id_c2586920
    on tickets_subcategory (category_id);

create index if not exists tickets_subcategory_scat_author_id_0acaf9ac
    on tickets_subcategory (scat_author_id);

create index if not exists tickets_subcategory_scat_status_id_c8b91926
    on tickets_subcategory (scat_status_id);

create table if not exists tickets_ticket
(
    ticket_id         serial                   not null
        constraint tickets_ticket_pkey
            primary key,
    ticket_code       varchar(50)              not null,
    title             varchar(50)              not null,
    description       text                     not null,
    last_update       timestamp with time zone not null,
    date_added        timestamp with time zone not null,
    category_id       integer                  not null
        constraint tickets_ticket_category_id_710dbfd0_fk_tickets_category_cat_id
            references tickets_category
            deferrable initially deferred,
    client_id         integer                  not null
        constraint tickets_ticket_client_id_33a3e09e_fk_tickets_client_client_id
            references tickets_client
            deferrable initially deferred,
    hot_issue_id      integer
        constraint tickets_ticket_hot_issue_id_de346bd4_fk_tickets_hotissue_hi_id
            references tickets_hotissue
            deferrable initially deferred,
    last_update_by_id integer                  not null
        constraint tickets_ticket_last_update_by_id_d037bf51_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    module_id         integer                  not null
        constraint tickets_ticket_module_id_0e635ba3_fk_tickets_module_mod_id
            references tickets_module
            deferrable initially deferred,
    product_id        integer                  not null
        constraint tickets_ticket_product_id_ce107858_fk_tickets_product_prod_id
            references tickets_product
            deferrable initially deferred,
    project_id        integer                  not null
        constraint tickets_ticket_project_id_9d54a0fb_fk_tickets_project_proj_id
            references tickets_project
            deferrable initially deferred,
    status_id         integer                  not null
        constraint tickets_ticket_status_id_e7d9f42f_fk_tickets_status_stat_id
            references tickets_status
            deferrable initially deferred,
    sub_category_id   integer                  not null
        constraint tickets_ticket_sub_category_id_1c6ee3c8_fk_tickets_s
            references tickets_subcategory
            deferrable initially deferred,
    ticket_author_id  integer                  not null
        constraint tickets_ticket_ticket_author_id_09afbfa0_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred,
    ticket_owner_id   integer                  not null
        constraint tickets_ticket_ticket_owner_id_17afe13c_fk_users_team_team_id
            references users_team
            deferrable initially deferred,
    solution_id       integer
        constraint tickets_ticket_solution_id_defc1b9b_fk_tickets_c
            references tickets_comment
            deferrable initially deferred,
    date_closed       timestamp with time zone,
    closed_by_id      integer
        constraint tickets_ticket_closed_by_id_e398ed81_fk_users_customuser_id
            references users_customuser
            deferrable initially deferred
);

alter table tickets_ticket
    owner to kent;

alter table tickets_comment
    add constraint tickets_comment_ticket_id_36a9497d_fk_tickets_ticket_ticket_id
        foreign key (ticket_id) references tickets_ticket
            deferrable initially deferred;

create index if not exists tickets_ticket_category_id_710dbfd0
    on tickets_ticket (category_id);

create index if not exists tickets_ticket_client_id_33a3e09e
    on tickets_ticket (client_id);

create index if not exists tickets_ticket_hot_issue_id_de346bd4
    on tickets_ticket (hot_issue_id);

create index if not exists tickets_ticket_last_update_by_id_d037bf51
    on tickets_ticket (last_update_by_id);

create index if not exists tickets_ticket_module_id_0e635ba3
    on tickets_ticket (module_id);

create index if not exists tickets_ticket_product_id_ce107858
    on tickets_ticket (product_id);

create index if not exists tickets_ticket_project_id_9d54a0fb
    on tickets_ticket (project_id);

create index if not exists tickets_ticket_status_id_e7d9f42f
    on tickets_ticket (status_id);

create index if not exists tickets_ticket_sub_category_id_1c6ee3c8
    on tickets_ticket (sub_category_id);

create index if not exists tickets_ticket_ticket_author_id_09afbfa0
    on tickets_ticket (ticket_author_id);

create index if not exists tickets_ticket_ticket_owner_id_17afe13c
    on tickets_ticket (ticket_owner_id);

create index if not exists tickets_ticket_solution_id_defc1b9b
    on tickets_ticket (solution_id);

create index if not exists tickets_ticket_closed_by_id_e398ed81
    on tickets_ticket (closed_by_id);

create table if not exists tickets_ticketattachment
(
    attachment_id  serial       not null
        constraint tickets_ticketattachment_pkey
            primary key,
    file           varchar(100) not null,
    uploaded_on    timestamp with time zone,
    ticket_id      integer      not null
        constraint tickets_ticketattach_ticket_id_55842ab7_fk_tickets_t
            references tickets_ticket
            deferrable initially deferred,
    uploaded_by_id integer      not null
        constraint tickets_ticketattach_uploaded_by_id_3ee58633_fk_users_cus
            references users_customuser
            deferrable initially deferred
);

alter table tickets_ticketattachment
    owner to kent;

create index if not exists tickets_ticketattachment_ticket_id_55842ab7
    on tickets_ticketattachment (ticket_id);

create index if not exists tickets_ticketattachment_uploaded_by_id_3ee58633
    on tickets_ticketattachment (uploaded_by_id);

create table if not exists tickets_yearlyreport
(
    id serial not null
        constraint tickets_yearlyreport_pkey
            primary key
);

alter table tickets_yearlyreport
    owner to kent;

create table if not exists django_migrations
(
    id      serial                   not null
        constraint django_migrations_pkey
            primary key,
    app     varchar(255)             not null,
    name    varchar(255)             not null,
    applied timestamp with time zone not null
);

alter table django_migrations
    owner to kent;

create table if not exists django_content_type
(
    id        serial       not null
        constraint django_content_type_pkey
            primary key,
    app_label varchar(100) not null,
    model     varchar(100) not null,
    constraint django_content_type_app_label_model_76bd3d3b_uniq
        unique (app_label, model)
);

alter table django_content_type
    owner to kent;

create table if not exists auth_permission
(
    id              serial       not null
        constraint auth_permission_pkey
            primary key,
    name            varchar(255) not null,
    content_type_id integer      not null
        constraint auth_permission_content_type_id_2f476e4b_fk_django_co
            references django_content_type
            deferrable initially deferred,
    codename        varchar(100) not null,
    constraint auth_permission_content_type_id_codename_01ab375a_uniq
        unique (content_type_id, codename)
);

alter table auth_permission
    owner to kent;

create index if not exists auth_permission_content_type_id_2f476e4b
    on auth_permission (content_type_id);

create table if not exists auth_group
(
    id   serial       not null
        constraint auth_group_pkey
            primary key,
    name varchar(150) not null
        constraint auth_group_name_key
            unique
);

alter table auth_group
    owner to kent;

create index if not exists auth_group_name_a6ea08ec_like
    on auth_group (name);

create table if not exists auth_group_permissions
(
    id            serial  not null
        constraint auth_group_permissions_pkey
            primary key,
    group_id      integer not null
        constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
            references auth_group
            deferrable initially deferred,
    permission_id integer not null
        constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
            references auth_permission
            deferrable initially deferred,
    constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
        unique (group_id, permission_id)
);

alter table auth_group_permissions
    owner to kent;

create index if not exists auth_group_permissions_group_id_b120cbf9
    on auth_group_permissions (group_id);

create index if not exists auth_group_permissions_permission_id_84c5c92e
    on auth_group_permissions (permission_id);

create table if not exists tickets_producttype
(
    prod_type_id                serial                   not null
        constraint tickets_producttype_pkey
            primary key,
    prod_type_code              varchar(20)              not null,
    prod_type_name              varchar(25)              not null,
    prod_type_description       varchar(250)             not null,
    prod_type_last_update       timestamp with time zone not null,
    prod_type_date_added        timestamp with time zone not null,
    prod_type_author_id         integer                  not null
        constraint tickets_producttype_prod_type_author_id_16a5762c_fk_users_cus
            references users_customuser
            deferrable initially deferred,
    prod_type_last_update_by_id integer
        constraint tickets_producttype_prod_type_last_updat_269f05c3_fk_users_cus
            references users_customuser
            deferrable initially deferred
);

alter table tickets_producttype
    owner to kent;

create index if not exists tickets_producttype_prod_type_author_id_16a5762c
    on tickets_producttype (prod_type_author_id);

create index if not exists tickets_producttype_prod_type_last_update_by_id_269f05c3
    on tickets_producttype (prod_type_last_update_by_id);

