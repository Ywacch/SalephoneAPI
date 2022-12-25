--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;


--
-- Name: listings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.listings (
    item_id character varying(12) NOT NULL,
    title character varying NOT NULL,
    global_id character varying,
    product_id character varying,
    postal_code character varying,
    location_ character varying,
    country character varying,
    currency character varying,
    price numeric,
    condition_ character varying,
    shipping_type character varying,
    shipping_currency character varying,
    shipping_cost numeric,
    top_rated boolean,
    start_date date,
    end_date date,
    listing_type character varying,
    date_added date NOT NULL,
    canadian_price_base numeric,
    canadian_total numeric
);


ALTER TABLE public.listings OWNER TO postgres;

--
-- Name: phonelistings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.phonelistings (
    phone_id character varying(32) NOT NULL,
    item_id character varying(12) NOT NULL,
    date_added date NOT NULL
);


ALTER TABLE public.phonelistings OWNER TO postgres;

--
-- Name: smartphones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.smartphones (
    phone_id character varying(32) NOT NULL,
    brand character varying,
    series character varying,
    model character varying,
    phone_name character varying,
    storage_size character varying
);


ALTER TABLE public.smartphones OWNER TO postgres;



--
-- Name: listings listings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listings
    ADD CONSTRAINT listings_pkey PRIMARY KEY (item_id, date_added);


--
-- Name: phonelistings phonelistings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phonelistings
    ADD CONSTRAINT phonelistings_pkey PRIMARY KEY (phone_id, item_id, date_added);


--
-- Name: smartphones smartphones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.smartphones
    ADD CONSTRAINT smartphones_pkey PRIMARY KEY (phone_id);



--
-- Name: phonelistings phonelistings_item_id_date_added_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phonelistings
    ADD CONSTRAINT phonelistings_item_id_date_added_fkey FOREIGN KEY (item_id, date_added) REFERENCES public.listings(item_id, date_added) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: phonelistings phonelistings_phone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phonelistings
    ADD CONSTRAINT phonelistings_phone_id_fkey FOREIGN KEY (phone_id) REFERENCES public.smartphones(phone_id) ON UPDATE CASCADE;


--
-- PostgreSQL database dump complete
--


-- Postgres subscription creation goes here:

