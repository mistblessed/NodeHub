--
-- PostgreSQL database dump
--

\restrict 4dbQ4pXAAQBgzuJTWCKuzCToaKv0izaMRYOscZeaIx1CnaT58M62p2xAtWailg9

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-05-20 14:53:13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 220 (class 1259 OID 25362)
-- Name: feedback; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.feedback (
    id integer NOT NULL,
    user_id integer,
    name character varying(100),
    email character varying(120),
    subject character varying(200) NOT NULL,
    message text NOT NULL,
    status character varying(20) DEFAULT 'new'::character varying,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT feedback_status_check CHECK (((status)::text = ANY ((ARRAY['new'::character varying, 'read'::character varying, 'replied'::character varying])::text[])))
);


ALTER TABLE public.feedback OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 25361)
-- Name: feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.feedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feedback_id_seq OWNER TO postgres;

--
-- TOC entry 5020 (class 0 OID 0)
-- Dependencies: 219
-- Name: feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.feedback_id_seq OWNED BY public.feedback.id;


--
-- TOC entry 221 (class 1259 OID 26622)
-- Name: lessons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lessons (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    theoretical_content text NOT NULL,
    "order" integer DEFAULT 0 NOT NULL,
    module_id integer NOT NULL
);


ALTER TABLE public.lessons OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 26633)
-- Name: lessons_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.lessons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.lessons_id_seq OWNER TO postgres;

--
-- TOC entry 5021 (class 0 OID 0)
-- Dependencies: 222
-- Name: lessons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.lessons_id_seq OWNED BY public.lessons.id;


--
-- TOC entry 223 (class 1259 OID 26634)
-- Name: modules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.modules (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    "order" integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.modules OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 26643)
-- Name: modules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.modules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.modules_id_seq OWNER TO postgres;

--
-- TOC entry 5022 (class 0 OID 0)
-- Dependencies: 224
-- Name: modules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.modules_id_seq OWNED BY public.modules.id;


--
-- TOC entry 225 (class 1259 OID 26644)
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    text text NOT NULL,
    question_type character varying(30) NOT NULL,
    options jsonb,
    correct_answer text NOT NULL,
    test_id integer NOT NULL,
    CONSTRAINT questions_question_type_check CHECK (((question_type)::text = ANY (ARRAY[('single_choice'::character varying)::text, ('multiple_choice'::character varying)::text, ('text_input'::character varying)::text])))
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 26655)
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.questions_id_seq OWNER TO postgres;

--
-- TOC entry 5023 (class 0 OID 0)
-- Dependencies: 226
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- TOC entry 227 (class 1259 OID 26656)
-- Name: tests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tests (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    module_id integer NOT NULL
);


ALTER TABLE public.tests OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 26662)
-- Name: tests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tests_id_seq OWNER TO postgres;

--
-- TOC entry 5024 (class 0 OID 0)
-- Dependencies: 228
-- Name: tests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tests_id_seq OWNED BY public.tests.id;


--
-- TOC entry 229 (class 1259 OID 26663)
-- Name: user_answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_answers (
    id integer NOT NULL,
    user_id integer NOT NULL,
    question_id integer NOT NULL,
    given_answer text NOT NULL,
    is_correct boolean NOT NULL,
    answered_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.user_answers OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 26674)
-- Name: user_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_answers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_answers_id_seq OWNER TO postgres;

--
-- TOC entry 5025 (class 0 OID 0)
-- Dependencies: 230
-- Name: user_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_answers_id_seq OWNED BY public.user_answers.id;


--
-- TOC entry 231 (class 1259 OID 26675)
-- Name: user_progress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_progress (
    id integer NOT NULL,
    user_id integer NOT NULL,
    lesson_id integer,
    test_id integer,
    status character varying(30) DEFAULT 'in_progress'::character varying NOT NULL,
    score real,
    completed_at timestamp with time zone DEFAULT now(),
    CONSTRAINT chk_progress_object CHECK ((((lesson_id IS NOT NULL) AND (test_id IS NULL)) OR ((lesson_id IS NULL) AND (test_id IS NOT NULL)))),
    CONSTRAINT user_progress_status_check CHECK (((status)::text = ANY (ARRAY[('in_progress'::character varying)::text, ('completed'::character varying)::text, ('failed'::character varying)::text])))
);


ALTER TABLE public.user_progress OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 26685)
-- Name: user_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_progress_id_seq OWNER TO postgres;

--
-- TOC entry 5026 (class 0 OID 0)
-- Dependencies: 232
-- Name: user_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_progress_id_seq OWNED BY public.user_progress.id;


--
-- TOC entry 233 (class 1259 OID 26686)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) DEFAULT 'student'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT users_role_check CHECK (((role)::text = ANY (ARRAY[('student'::character varying)::text, ('admin'::character varying)::text])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 26697)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5027 (class 0 OID 0)
-- Dependencies: 234
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4790 (class 2604 OID 26698)
-- Name: feedback id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedback ALTER COLUMN id SET DEFAULT nextval('public.feedback_id_seq'::regclass);


--
-- TOC entry 4793 (class 2604 OID 26699)
-- Name: lessons id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lessons ALTER COLUMN id SET DEFAULT nextval('public.lessons_id_seq'::regclass);


--
-- TOC entry 4795 (class 2604 OID 26700)
-- Name: modules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules ALTER COLUMN id SET DEFAULT nextval('public.modules_id_seq'::regclass);


--
-- TOC entry 4797 (class 2604 OID 26701)
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- TOC entry 4798 (class 2604 OID 26702)
-- Name: tests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tests ALTER COLUMN id SET DEFAULT nextval('public.tests_id_seq'::regclass);


--
-- TOC entry 4799 (class 2604 OID 26703)
-- Name: user_answers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_answers ALTER COLUMN id SET DEFAULT nextval('public.user_answers_id_seq'::regclass);


--
-- TOC entry 4801 (class 2604 OID 26704)
-- Name: user_progress id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_progress ALTER COLUMN id SET DEFAULT nextval('public.user_progress_id_seq'::regclass);


--
-- TOC entry 4804 (class 2604 OID 26705)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5000 (class 0 OID 25362)
-- Dependencies: 220
-- Data for Name: feedback; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.feedback (id, user_id, name, email, subject, message, status, created_at) FROM stdin;
\.


--
-- TOC entry 5001 (class 0 OID 26622)
-- Dependencies: 221
-- Data for Name: lessons; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lessons (id, title, theoretical_content, "order", module_id) FROM stdin;
1	Что такое Node.js?	\n<h2>Что такое Node.js?</h2>\n<p>Node.js — это среда выполнения JavaScript, построенная на движке V8 от Google. Она позволяет запускать JavaScript-код на сервере, вне браузера.</p>\n<h3>Ключевые особенности</h3>\n<ul>\n  <li><strong>Событийно-ориентированная архитектура</strong> — все операции ввода-вывода не блокируют поток выполнения.</li>\n  <li><strong>Асинхронность</strong> — использует колбэки, промисы и async/await.</li>\n  <li><strong>Однопоточность</strong> — основной цикл событий работает в одном потоке, но тяжёлые задачи можно выносить в отдельные потоки (worker_threads).</li>\n</ul>\n<p>Node.js широко применяется для создания веб-серверов, API, микросервисов, инструментов сборки и реального времени (чаты, игры).</p>\n<pre><code class="language-javascript">// Простейший сервер на Node.js\nconst http = require('http');\nconst server = http.createServer((req, res) => {\n  res.writeHead(200, {'Content-Type': 'text/plain'});\n  res.end('Hello, world!');\n});\nserver.listen(3000, () => console.log('Сервер запущен на порту 3000'));\n</code></pre>	1	1
2	Установка и настройка окружения	\n<h2>Установка и настройка окружения</h2>\n<p>Скачайте последнюю <strong>LTS-версию</strong> Node.js с официального сайта <a href="https://nodejs.org" target="_blank">nodejs.org</a>.</p>\n<p>После установки проверьте версии командной строкой:</p>\n<pre><code class="language-bash">node -v\nnpm -v\n</code></pre>\n<p>npm (Node Package Manager) устанавливается автоматически вместе с Node.js и служит для управления зависимостями.</p>\n<p>Рекомендуется также использовать менеджер версий <code>nvm</code> (для Linux/Mac) или <code>nvm-windows</code>, чтобы легко переключаться между версиями.</p>	2	1
3	Первое приложение: Hello World	\n<h2>Первое приложение: Hello World</h2>\n<p>Создайте файл <code>app.js</code> со следующим содержимым:</p>\n<pre><code class="language-javascript">console.log("Hello, Node.js!");\n</code></pre>\n<p>Запустите его через терминал:</p>\n<pre><code class="language-bash">node app.js\n</code></pre>\n<p>Вы увидите вывод в консоли. Это минимальное Node.js приложение.</p>\n<h3>Работа с REPL</h3>\n<p>Node.js имеет встроенный интерактивный режим REPL (<em>Read-Eval-Print Loop</em>). Просто введите <code>node</code> без аргументов и можете выполнять JavaScript построчно.</p>\n<pre><code class="language-bash">node\n> 2 + 2\n4\n</code></pre>	3	1
4	Глобальные объекты и process	\n<h2>Глобальные объекты и process</h2>\n<p>В Node.js доступны следующие глобальные объекты (аналоги <code>window</code> в браузере):</p>\n<ul>\n  <li><code>__dirname</code> — путь к текущей директории.</li>\n  <li><code>__filename</code> — полный путь к текущему файлу.</li>\n  <li><code>process</code> — информация о текущем процессе.</li>\n</ul>\n<h3>Объект process</h3>\n<p>Содержит свойства и методы для взаимодействия с процессом Node.js:</p>\n<pre><code class="language-javascript">console.log(process.version);  // версия Node.js\nconsole.log(process.argv);     // аргументы командной строки\nconsole.log(process.cwd());    // текущая рабочая директория\n</code></pre>\n<p>Переменные окружения доступны через <code>process.env</code>.</p>\n<pre><code class="language-javascript">const port = process.env.PORT || 3000;\n</code></pre>	4	1
5	Модульная система CommonJS	\n<h2>Модульная система CommonJS</h2>\n<p>Node.js использует систему модулей <strong>CommonJS</strong>. Каждый файл считается модулем.</p>\n<ul>\n  <li><code>require()</code> — импорт модуля.</li>\n  <li><code>module.exports</code> или <code>exports</code> — экспорт функциональности.</li>\n</ul>\n<pre><code class="language-javascript">// file math.js\nfunction add(a, b) {\n  return a + b;\n}\nmodule.exports = { add };\n</code></pre>\n<pre><code class="language-javascript">// main.js\nconst math = require('./math');\nconsole.log(math.add(2, 3)); // 5\n</code></pre>\n<p>Существуют также <strong>ES-модули</strong> (import/export), которые можно активировать флагом <code>"type": "module"</code> в package.json или расширением <code>.mjs</code>.</p>	1	2
6	Создание и подключение модулей	\n<h2>Создание и подключение модулей</h2>\n<p>Создайте свой модуль, например, для работы с датами. Экспортируйте нужные функции, а затем импортируйте их в основном файле.</p>\n<pre><code class="language-javascript">// dateUtils.js\nfunction formatDate(date) {\n  return date.toISOString().slice(0, 10);\n}\nexports.formatDate = formatDate;\n</code></pre>\n<p>Использование:</p>\n<pre><code class="language-javascript">const { formatDate } = require('./dateUtils');\nconsole.log(formatDate(new Date())); // "2026-05-10"\n</code></pre>\n<p>Помните: путь к собственному модулю начинается с <code>./</code> или <code>../</code>, а для встроенных или установленных через npm — без префикса.</p>	2	2
7	Работа с NPM и package.json	\n<h2>Работа с NPM и package.json</h2>\n<p><strong>npm</strong> — менеджер пакетов, поставляемый с Node.js. Команда <code>npm init</code> создаёт файл <code>package.json</code>, который хранит метаданные проекта и зависимости.</p>\n<pre><code class="language-json">{\n  "name": "my-project",\n  "version": "1.0.0",\n  "main": "index.js",\n  "scripts": {\n    "start": "node index.js"\n  },\n  "dependencies": {\n    "express": "^4.18.2"\n  }\n}\n</code></pre>\n<p>Основные команды:</p>\n<ul>\n  <li><code>npm install</code> — установить все зависимости из package.json</li>\n  <li><code>npm install &lt;package&gt;</code> — добавить пакет в зависимости</li>\n  <li><code>npm uninstall &lt;package&gt;</code> — удалить</li>\n</ul>	3	2
8	Установка и использование пакетов	\n<h2>Установка и использование пакетов</h2>\n<p>Популярные пакеты:</p>\n<ul>\n  <li><strong>lodash</strong> — утилиты для работы с данными</li>\n  <li><strong>axios</strong> — HTTP-клиент</li>\n  <li><strong>express</strong> — веб-фреймворк</li>\n</ul>\n<pre><code class="language-bash">npm install axios\n</code></pre>\n<pre><code class="language-javascript">const axios = require('axios');\naxios.get('https://api.example.com/data')\n  .then(response => console.log(response.data))\n  .catch(error => console.error(error));\n</code></pre>\n<p>Установленные пакеты размещаются в папке <code>node_modules</code> (её не нужно коммитить в Git).</p>	4	2
9	Встроенный модуль http	\n<h2>Встроенный модуль http</h2>\n<p>Модуль <code>http</code> позволяет создавать веб-серверы без внешних зависимостей.</p>\n<pre><code class="language-javascript">const http = require('http');\nconst server = http.createServer((req, res) => {\n  res.writeHead(200, {'Content-Type': 'text/plain'});\n  res.end('Hello World');\n});\nserver.listen(3000, () => console.log('Сервер запущен'));\n</code></pre>\n<p>Метод <code>createServer()</code> принимает callback с двумя параметрами: <code>request</code> (объект запроса) и <code>response</code> (объект ответа).</p>	1	3
10	Обработка запросов и ответов	\n<h2>Обработка запросов и ответов</h2>\n<p>Объект <code>request</code> содержит URL, метод, заголовки и тело запроса.</p>\n<pre><code class="language-javascript">const server = http.createServer((req, res) => {\n  console.log(req.url, req.method);\n  if (req.method === 'GET') {\n    res.writeHead(200, {'Content-Type': 'text/html'});\n    res.end('<h1>Главная</h1>');\n  } else {\n    res.writeHead(405);\n    res.end();\n  }\n});\n</code></pre>\n<p>Тело POST-запроса собирается через события <code>data</code> и <code>end</code>.</p>	2	3
11	Маршрутизация	\n<h2>Маршрутизация</h2>\n<p>Простейшая маршрутизация реализуется проверкой <code>req.url</code>. Однако для сложных приложений удобнее использовать фреймворки.</p>\n<pre><code class="language-javascript">const server = http.createServer((req, res) => {\n  if (req.url === '/') {\n    res.writeHead(200, {'Content-Type': 'text/plain'});\n    res.end('Главная страница');\n  } else if (req.url === '/about') {\n    res.writeHead(200, {'Content-Type': 'text/plain'});\n    res.end('О нас');\n  } else {\n    res.writeHead(404);\n    res.end('Не найдено');\n  }\n});\n</code></pre>	3	3
12	Основы Express.js	\n<h2>Основы Express.js</h2>\n<p>Express — минималистичный веб-фреймворк для Node.js. Установка:</p>\n<pre><code class="language-bash">npm install express\n</code></pre>\n<p>Создайте файл <code>server.js</code>:</p>\n<pre><code class="language-javascript">const express = require('express');\nconst app = express();\napp.get('/', (req, res) => {\n  res.send('Hello Express!');\n});\napp.listen(3000, () => console.log('Сервер на порту 3000'));\n</code></pre>\n<p>Express предлагает удобную маршрутизацию, middleware и интеграцию с шаблонизаторами.</p>	4	3
\.


--
-- TOC entry 5003 (class 0 OID 26634)
-- Dependencies: 223
-- Data for Name: modules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.modules (id, title, description, "order") FROM stdin;
1	Основы Node.js	Введение в платформу, установка и первые шаги.	1
3	Создание HTTP-сервера	Встроенные модули http, маршрутизация и Express.	3
2	Работа с модулями и NPM!	Система модулей, менеджер пакетов и экосистема.	2
\.


--
-- TOC entry 5005 (class 0 OID 26644)
-- Dependencies: 225
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (id, text, question_type, options, correct_answer, test_id) FROM stdin;
16	На каком движке работает Node.js?	single_choice	["V8", "SpiderMonkey", "Chakra", "JavaScriptCore"]	V8	4
17	Какая команда запускает JS-файл в Node.js?	single_choice	["node file.js", "npm file.js", "nodejs file.js", "run file.js"]	node file.js	4
18	Что делает объект process? (выберите несколько)	multiple_choice	["Предоставляет информацию о процессе", "Управляет DOM-деревом", "Содержит переменные окружения", "Отвечает за рендеринг страницы"]	["Предоставляет информацию о процессе", "Содержит переменные окружения"]	4
19	Node.js является однопоточным.	single_choice	["Верно", "Неверно"]	Верно	4
20	Напишите команду для проверки версии Node.js	text_input	\N	node -v	4
21	Какой метод используется для импорта модулей в CommonJS?	single_choice	["import", "require", "include", "using"]	require	5
22	Что создаёт команда npm init?	single_choice	["node_modules", "package.json", "index.js", "README.md"]	package.json	5
23	Выберите корректные способы экспорта из модуля:	multiple_choice	["module.exports = myFunc", "exports.myFunc = myFunc", "export default myFunc", "export { myFunc }"]	["module.exports = myFunc", "exports.myFunc = myFunc"]	5
24	Пакеты, установленные через npm, хранятся в папке:	single_choice	["packages", "node_modules", "libs", "assets"]	node_modules	5
25	Напишите точную команду для установки пакета express	text_input	\N	npm install express	5
26	Какой встроенный модуль Node.js используется для создания веб-сервера?	single_choice	["fs", "http", "url", "net"]	http	6
27	Метод res.writeHead() позволяет:	single_choice	["Установить статус-код и заголовки", "Записать данные в файл", "Закрыть соединение", "Начать новый запрос"]	Установить статус-код и заголовки	6
28	Какие HTTP-методы обычно используются в REST API?	multiple_choice	["GET", "POST", "PUT", "DELETE", "FETCH"]	["GET", "POST", "PUT", "DELETE"]	6
29	Express.js — это:	single_choice	["Встроенный модуль Node.js", "Веб-фреймворк для Node.js", "База данных", "Язык программирования"]	Веб-фреймворк для Node.js	6
30	Введите стандартный порт, на котором обычно запускают Express-приложение в учебных примерах	text_input	\N	3000	6
\.


--
-- TOC entry 5007 (class 0 OID 26656)
-- Dependencies: 227
-- Data for Name: tests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tests (id, title, module_id) FROM stdin;
4	Тест: Основы Node.js	1
5	Тест: Модули и NPM	2
6	Тест: HTTP и Express	3
\.


--
-- TOC entry 5009 (class 0 OID 26663)
-- Dependencies: 229
-- Data for Name: user_answers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_answers (id, user_id, question_id, given_answer, is_correct, answered_at) FROM stdin;
6	3	16	V8	t	2026-05-10 11:37:13.648972+03
7	3	17	run file.js	f	2026-05-10 11:37:13.654726+03
8	3	18	Отвечает за рендеринг страницы	f	2026-05-10 11:37:13.655897+03
9	3	19	Неверно	f	2026-05-10 11:37:13.65675+03
10	3	20	123	f	2026-05-10 11:37:13.657545+03
11	3	16	V8	t	2026-05-10 12:48:04.933472+03
12	3	18	Предоставляет информацию о процессе	f	2026-05-10 12:48:04.935543+03
13	3	20	123	f	2026-05-10 12:48:04.936476+03
14	3	16	V8	t	2026-05-10 12:48:21.089757+03
15	3	17	run file.js	f	2026-05-10 12:48:21.091091+03
16	3	18	Управляет DOM-деревом	f	2026-05-10 12:48:21.092209+03
17	3	19	Неверно	f	2026-05-10 12:48:21.093423+03
18	3	20	123	f	2026-05-10 12:48:21.094504+03
19	5	16	V8	t	2026-05-10 13:34:30.557624+03
20	5	17	node file.js	t	2026-05-10 13:34:30.570289+03
21	5	18	Управляет DOM-деревом	f	2026-05-10 13:34:30.571563+03
22	5	19	Верно	t	2026-05-10 13:34:30.572795+03
23	5	20	123	f	2026-05-10 13:34:30.573869+03
24	4	16	V8	t	2026-05-10 22:17:11.882604+03
25	4	17	run file.js	f	2026-05-10 22:17:11.94999+03
26	4	18	Управляет DOM-деревом	f	2026-05-10 22:17:11.951351+03
27	4	19	Неверно	f	2026-05-10 22:17:11.952552+03
28	4	20	version	f	2026-05-10 22:17:11.953699+03
29	3	16	V8	t	2026-05-11 19:35:26.622765+03
30	3	17	node file.js	t	2026-05-11 19:35:26.719666+03
31	3	18	Предоставляет информацию о процессе	f	2026-05-11 19:35:26.737968+03
32	3	19	Неверно	f	2026-05-11 19:35:26.739527+03
33	3	20	123	f	2026-05-11 19:35:26.740601+03
\.


--
-- TOC entry 5011 (class 0 OID 26675)
-- Dependencies: 231
-- Data for Name: user_progress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_progress (id, user_id, lesson_id, test_id, status, score, completed_at) FROM stdin;
6	3	4	\N	completed	\N	2026-05-10 11:37:01.566746+03
8	3	1	\N	completed	\N	2026-05-10 12:42:33.181979+03
9	5	1	\N	completed	\N	2026-05-10 13:34:16.575389+03
10	5	3	\N	completed	\N	2026-05-10 13:34:18.224948+03
11	5	\N	4	completed	60	2026-05-10 13:34:30.556139+03
12	4	1	\N	completed	\N	2026-05-10 22:16:20.259881+03
13	4	2	\N	completed	\N	2026-05-10 22:16:23.940496+03
14	4	3	\N	completed	\N	2026-05-10 22:16:26.306929+03
15	4	4	\N	completed	\N	2026-05-10 22:16:27.972622+03
16	4	\N	4	completed	20	2026-05-10 22:17:11.847846+03
17	3	2	\N	completed	\N	2026-05-11 19:34:48.702601+03
7	3	\N	4	completed	40	2026-05-11 19:35:26.324648+03
\.


--
-- TOC entry 5013 (class 0 OID 26686)
-- Dependencies: 233
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, role, created_at) FROM stdin;
3	mist	sadovnikof2018@yandex.ru	$2b$12$66QBYLFQ41ojE4YjeVwMyu0Awxh91VcJRTN.MKtBSr87ZtBjLLgGy	admin	2026-05-10 11:34:48.696932+03
4	admin	admin@gmail.com	$2b$12$V2rBvwHvn5VgTgBPHNeraeyCxrdDdBXq26TGc7L2NBSQkEMJspa9O	admin	2026-05-10 11:39:24.817126+03
5	student	student@gmail.com	$2b$12$h5WzQqkngdYQsLPMpWfKUultcBSqzcmX9VeQPr4j3rz7n2MWoe4jC	student	2026-05-10 11:39:55.273129+03
6	privet	privet@yandex.ru	$2b$12$./SaSlU/sN76svZJq6I5MOajlFP40jTkxYUsM6Vl8QdTFnj5klKjq	student	2026-05-17 12:46:13.431696+03
\.


--
-- TOC entry 5028 (class 0 OID 0)
-- Dependencies: 219
-- Name: feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.feedback_id_seq', 5, true);


--
-- TOC entry 5029 (class 0 OID 0)
-- Dependencies: 222
-- Name: lessons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.lessons_id_seq', 12, true);


--
-- TOC entry 5030 (class 0 OID 0)
-- Dependencies: 224
-- Name: modules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.modules_id_seq', 3, true);


--
-- TOC entry 5031 (class 0 OID 0)
-- Dependencies: 226
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questions_id_seq', 30, true);


--
-- TOC entry 5032 (class 0 OID 0)
-- Dependencies: 228
-- Name: tests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tests_id_seq', 6, true);


--
-- TOC entry 5033 (class 0 OID 0)
-- Dependencies: 230
-- Name: user_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_answers_id_seq', 33, true);


--
-- TOC entry 5034 (class 0 OID 0)
-- Dependencies: 232
-- Name: user_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_progress_id_seq', 17, true);


--
-- TOC entry 5035 (class 0 OID 0)
-- Dependencies: 234
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- TOC entry 4813 (class 2606 OID 25375)
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (id);


--
-- TOC entry 4817 (class 2606 OID 26707)
-- Name: lessons lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_pkey PRIMARY KEY (id);


--
-- TOC entry 4820 (class 2606 OID 26709)
-- Name: modules modules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_pkey PRIMARY KEY (id);


--
-- TOC entry 4823 (class 2606 OID 26711)
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- TOC entry 4826 (class 2606 OID 26713)
-- Name: tests tests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_pkey PRIMARY KEY (id);


--
-- TOC entry 4830 (class 2606 OID 26715)
-- Name: user_answers user_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_answers
    ADD CONSTRAINT user_answers_pkey PRIMARY KEY (id);


--
-- TOC entry 4835 (class 2606 OID 26717)
-- Name: user_progress user_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_progress
    ADD CONSTRAINT user_progress_pkey PRIMARY KEY (id);


--
-- TOC entry 4839 (class 2606 OID 26719)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4841 (class 2606 OID 26721)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4843 (class 2606 OID 26723)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4814 (class 1259 OID 26724)
-- Name: idx_lessons_module_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lessons_module_id ON public.lessons USING btree (module_id);


--
-- TOC entry 4815 (class 1259 OID 26725)
-- Name: idx_lessons_order; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lessons_order ON public.lessons USING btree ("order");


--
-- TOC entry 4818 (class 1259 OID 26726)
-- Name: idx_modules_order; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_modules_order ON public.modules USING btree ("order");


--
-- TOC entry 4821 (class 1259 OID 26727)
-- Name: idx_questions_test_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_questions_test_id ON public.questions USING btree (test_id);


--
-- TOC entry 4824 (class 1259 OID 26728)
-- Name: idx_tests_module_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tests_module_id ON public.tests USING btree (module_id);


--
-- TOC entry 4827 (class 1259 OID 26729)
-- Name: idx_user_answers_question; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_answers_question ON public.user_answers USING btree (question_id);


--
-- TOC entry 4828 (class 1259 OID 26730)
-- Name: idx_user_answers_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_answers_user ON public.user_answers USING btree (user_id);


--
-- TOC entry 4831 (class 1259 OID 26731)
-- Name: idx_user_progress_lesson; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_progress_lesson ON public.user_progress USING btree (lesson_id);


--
-- TOC entry 4832 (class 1259 OID 26732)
-- Name: idx_user_progress_test; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_progress_test ON public.user_progress USING btree (test_id);


--
-- TOC entry 4833 (class 1259 OID 26733)
-- Name: idx_user_progress_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_progress_user ON public.user_progress USING btree (user_id);


--
-- TOC entry 4836 (class 1259 OID 26734)
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_email ON public.users USING btree (email);


--
-- TOC entry 4837 (class 1259 OID 26735)
-- Name: idx_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_username ON public.users USING btree (username);


--
-- TOC entry 4844 (class 2606 OID 26741)
-- Name: lessons lessons_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id) ON DELETE CASCADE;


--
-- TOC entry 4845 (class 2606 OID 26746)
-- Name: questions questions_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.tests(id) ON DELETE CASCADE;


--
-- TOC entry 4846 (class 2606 OID 26751)
-- Name: tests tests_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id) ON DELETE CASCADE;


--
-- TOC entry 4847 (class 2606 OID 26756)
-- Name: user_answers user_answers_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_answers
    ADD CONSTRAINT user_answers_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id) ON DELETE CASCADE;


--
-- TOC entry 4848 (class 2606 OID 26761)
-- Name: user_answers user_answers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_answers
    ADD CONSTRAINT user_answers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 4849 (class 2606 OID 26766)
-- Name: user_progress user_progress_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_progress
    ADD CONSTRAINT user_progress_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE SET NULL;


--
-- TOC entry 4850 (class 2606 OID 26771)
-- Name: user_progress user_progress_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_progress
    ADD CONSTRAINT user_progress_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.tests(id) ON DELETE SET NULL;


--
-- TOC entry 4851 (class 2606 OID 26776)
-- Name: user_progress user_progress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_progress
    ADD CONSTRAINT user_progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


-- Completed on 2026-05-20 14:53:15

--
-- PostgreSQL database dump complete
--

\unrestrict 4dbQ4pXAAQBgzuJTWCKuzCToaKv0izaMRYOscZeaIx1CnaT58M62p2xAtWailg9

