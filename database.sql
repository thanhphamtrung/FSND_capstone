--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

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
-- Name: Actor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Actor" (
    id integer NOT NULL,
    name character varying,
    age integer,
    sex character varying,
    city character varying(120),
    state character varying(120),
    phone character varying(120),
    genres character varying(120),
    image_link character varying(500),
    website character varying(120),
    seeking_movie boolean,
    seeking_description character varying(1000),
    CONSTRAINT "Actor_age_check" CHECK (((age > 0) AND (age < 100)))
);


ALTER TABLE public."Actor" OWNER TO postgres;

--
-- Name: Actor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Actor_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Actor_id_seq" OWNER TO postgres;

--
-- Name: Actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Actor_id_seq" OWNED BY public."Actor".id;


--
-- Name: Casting; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Casting" (
    id integer NOT NULL,
    actor_id integer NOT NULL,
    movie_id integer NOT NULL,
    start_time timestamp without time zone,
    place character varying
);


ALTER TABLE public."Casting" OWNER TO postgres;

--
-- Name: Casting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Casting_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Casting_id_seq" OWNER TO postgres;

--
-- Name: Casting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Casting_id_seq" OWNED BY public."Casting".id;


--
-- Name: Movie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Movie" (
    id integer NOT NULL,
    name character varying,
    producer character varying,
    director character varying,
    phone character varying(120),
    image_link character varying(500),
    facebook_link character varying(120),
    genres character varying(120),
    website character varying(120),
    seeking_actor boolean,
    seeking_description character varying(1000)
);


ALTER TABLE public."Movie" OWNER TO postgres;

--
-- Name: Movie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Movie_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Movie_id_seq" OWNER TO postgres;

--
-- Name: Movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Movie_id_seq" OWNED BY public."Movie".id;


--
-- Name: Actor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Actor" ALTER COLUMN id SET DEFAULT nextval('public."Actor_id_seq"'::regclass);


--
-- Name: Casting id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Casting" ALTER COLUMN id SET DEFAULT nextval('public."Casting_id_seq"'::regclass);


--
-- Name: Movie id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Movie" ALTER COLUMN id SET DEFAULT nextval('public."Movie_id_seq"'::regclass);


--
-- Data for Name: Actor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Actor" (id, name, age, sex, city, state, phone, genres, image_link, website, seeking_movie, seeking_description) FROM stdin;
1	Arabela Lebbern	69	Female	Norman	Oklahoma	4056375359	Comedy|Drama|Romance|War	49.146.232.202	182.253.47.201	t	!@#$%^&*()
2	Amandi Grewcock	55	Female	Spartanburg	South Carolina	8641139421	Drama	175.158.204.166	65.11.237.63	t	
3	Jeff Petrushka	27	Male	New Castle	Pennsylvania	7247585798	Comedy|Crime|Romance	84.76.160.39	231.90.43.230	t	!@#$%^&*()
4	Deanne Stoop	66	Female	Washington	District of Columbia	2021128044	Comedy|Drama	64.228.170.161	91.204.23.103	t	-$1.00
5	Wally Gunby	59	Female	Hagerstown	Maryland	2409447191	Drama	3.89.218.203	157.54.82.226	f	''
6	Sheeree Jiruch	28	Female	San Diego	California	6197857756	Documentary	250.44.219.71	253.223.98.65	t	<svg><script>0<1>alert('XSS')</script>
7	Pet Dunsire	22	Female	Carol Stream	Illinois	3099466540	Drama	120.238.6.63	186.162.139.41	f	0.00
8	Stacey De Dei	30	Female	Fort Lauderdale	Florida	7543326887	Drama	79.89.37.191	144.12.125.46	t	00˙Ɩ$-
9	Jeni Hattigan	40	Female	Wilmington	North Carolina	9109634683	Crime|Drama|Romance|Thriller	68.35.225.141	160.46.139.97	f	!@#$%^&*()
10	Meagan Yankishin	55	Female	San Diego	California	6192906903	Drama	164.108.59.114	108.210.195.230	f	和製漢語
\.


--
-- Data for Name: Casting; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Casting" (id, actor_id, movie_id, start_time, place) FROM stdin;
1	10	7	2022-09-21 00:00:00	830 Eastwood Lane
2	7	2	2022-11-26 00:00:00	77 Basil Avenue
3	3	9	2022-07-19 00:00:00	98089 Moland Street
4	5	4	2022-09-24 00:00:00	81899 Holmberg Alley
5	7	10	2022-09-23 00:00:00	517 Almo Crossing
6	6	3	2023-01-27 00:00:00	2782 Ruskin Crossing
7	5	7	2023-06-06 00:00:00	8354 Mariners Cove Crossing
8	7	4	2022-07-28 00:00:00	0510 Nova Pass
9	8	6	2023-06-17 00:00:00	47711 Maryland Park
10	6	4	2022-07-28 00:00:00	843 Talisman Street
\.


--
-- Data for Name: Movie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Movie" (id, name, producer, director, phone, image_link, facebook_link, genres, website, seeking_actor, seeking_description) FROM stdin;
1	Dune	Dach-Streich	Seymour Huikerby	377 194 9960	193.29.250.56	32.193.119.161	Adventure|Sci-Fi	149.23.231.42	t	̗̺͖̹̯͓Ṯ̤͍̥͇͈h̲́e͏͓̼̗̙̼̣͔ ͇̜̱̠͓͍ͅN͕͠e̗̱z̘̝̜̺͙p̤̺̹͍̯͚e̠̻̠͜r̨̤͍̺̖͔̖̖d̠̟̭̬̝͟i̦͖̩͓͔̤a̠̗̬͉̙n͚͜ ̻̞̰͚ͅh̵͉i̳̞v̢͇ḙ͎͟-҉̭̩̼͔m̤̭̫i͕͇̝̦n̗͙ḍ̟ ̯̲͕͞ǫ̟̯̰̲͙̻̝f ̪̰̰̗̖̭̘͘c̦͍̲̞͍̩̙ḥ͚a̮͎̟̙͜ơ̩̹͎s̤.̝̝ ҉Z̡̖̜͖̰̣͉̜a͖̰͙̬͡l̲̫̳͍̩g̡̟̼̱͚̞̬ͅo̗͜.̟
2	A Magnificent Haunting	Dooley Group	Juliane Pexton	241 789 3774	27.215.169.113	166.11.226.15	Drama	190.29.216.110	t	˙ɐnbᴉlɐ ɐuƃɐɯ ǝɹolop ʇǝ ǝɹoqɐl ʇn ʇunpᴉpᴉɔuᴉ ɹodɯǝʇ poɯsnᴉǝ op pǝs 'ʇᴉlǝ ƃuᴉɔsᴉdᴉpɐ ɹnʇǝʇɔǝsuoɔ 'ʇǝɯɐ ʇᴉs ɹolop ɯnsdᴉ ɯǝɹo˥
3	Tree of Life, The	Kassulke and Sons	Tildie Bathersby	219 804 1843	175.127.40.17	212.213.102.248	Drama	120.113.99.140	t	-1E2
4	Cure, The	Crist-Homenick	Liesa Purcer	808 213 5010	225.204.174.38	182.178.231.79	Comedy	247.212.226.116	t	Z̮̞̠͙͔ͅḀ̗̞͈̻̗Ḷ͙͎̯̹̞͓G̻O̭̗̮
5	Beginner's Guide to Endings, A	Upton LLC	Arluene Merrifield	457 148 4376	45.135.116.71	108.84.152.221	Comedy|Drama	33.224.136.233	t	NIL
6	Men, Women & Children	Vandervort Inc	Leanora Doring	469 238 3531	154.33.127.39	6.227.186.118	Comedy|Drama	235.50.27.67	t	,。・:*:・゜’( ☻ ω ☻ )。・:*:・゜’
7	Yellow Submarine	Hartmann-Sawayn	Killie Fasey	593 731 0692	201.4.205.79	106.26.177.190	Adventure|Animation|Comedy|Fantasy|Musical	109.97.118.146	f	₀₁₂
8	Man in the Saddle	Renner-Schowalter	Enos Castelletto	578 813 9267	114.126.213.242	153.214.169.119	Western	248.86.194.40	f	1'; DROP TABLE users--
9	Dogfight	Kovacek and Sons	Jenine Lambourne	189 184 2036	211.9.97.167	203.196.177.183	Drama|Romance	226.11.138.151	f	社會科學院語學研究所
10	Formula, The	D'Amore LLC	Edan Cressingham	450 837 7771	33.78.196.235	169.12.109.100	Thriller	111.158.96.190	t	(╯°□°）╯︵ ┻━┻)  
\.


--
-- Name: Actor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Actor_id_seq"', 1, false);


--
-- Name: Casting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Casting_id_seq"', 1, false);


--
-- Name: Movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Movie_id_seq"', 1, false);


--
-- Name: Actor Actor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Actor"
    ADD CONSTRAINT "Actor_pkey" PRIMARY KEY (id);


--
-- Name: Casting Casting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Casting"
    ADD CONSTRAINT "Casting_pkey" PRIMARY KEY (id);


--
-- Name: Movie Movie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Movie"
    ADD CONSTRAINT "Movie_pkey" PRIMARY KEY (id);


--
-- Name: Casting Casting_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Casting"
    ADD CONSTRAINT "Casting_actor_id_fkey" FOREIGN KEY (actor_id) REFERENCES public."Actor"(id);


--
-- Name: Casting Casting_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Casting"
    ADD CONSTRAINT "Casting_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES public."Movie"(id);


--
-- PostgreSQL database dump complete
--

