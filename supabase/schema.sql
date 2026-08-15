-- Familia en Juego Cloud: esquema inicial.
-- Ejecutar solamente después de revisar el diseño y configurar el secreto backend.

create extension if not exists pgcrypto;

create table if not exists public.rooms (
  id uuid primary key default gen_random_uuid(),
  code text not null unique check (code ~ '^[A-Z0-9]{4,8}$'),
  host_secret_hash text not null,
  locale text not null default 'es' check (locale in ('es', 'pt-BR', 'en')),
  owner_id uuid references auth.users(id) on delete cascade,
  status text not null default 'lobby',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  expires_at timestamptz not null default (now() + interval '12 hours')
);

create table if not exists public.room_states (
  room_id uuid primary key references public.rooms(id) on delete cascade,
  version bigint not null default 1,
  state jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.players (
  id uuid primary key default gen_random_uuid(),
  room_id uuid not null references public.rooms(id) on delete cascade,
  name text not null check (char_length(name) between 1 and 40),
  team_id text,
  connection_token_hash text not null,
  online boolean not null default true,
  joined_at timestamptz not null default now(),
  last_seen_at timestamptz not null default now()
);

create index if not exists players_room_id_idx on public.players(room_id);
create unique index if not exists players_room_name_idx on public.players(room_id, lower(name));

create table if not exists public.content_cards (
  id uuid primary key default gen_random_uuid(),
  game text not null,
  difficulty text not null check (difficulty in ('facil', 'medio', 'dificil')),
  category text,
  content_key text not null unique,
  source_locale text not null default 'es' check (source_locale in ('es', 'pt-BR', 'en')),
  payload jsonb not null,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists content_cards_lookup_idx
  on public.content_cards(game, difficulty, active);

create table if not exists public.content_card_translations (
  card_id uuid not null references public.content_cards(id) on delete cascade,
  locale text not null check (locale in ('es', 'pt-BR', 'en')),
  category text,
  payload jsonb not null,
  reviewed boolean not null default false,
  updated_at timestamptz not null default now(),
  primary key (card_id, locale)
);

alter table public.rooms enable row level security;
alter table public.room_states enable row level security;
alter table public.players enable row level security;
alter table public.content_cards enable row level security;
alter table public.content_card_translations enable row level security;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null check (char_length(display_name) between 1 and 60),
  preferred_locale text not null default 'es' check (preferred_locale in ('es', 'pt-BR', 'en')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.game_sessions (
  id uuid primary key,
  owner_id uuid not null references auth.users(id) on delete cascade,
  room_id uuid references public.rooms(id) on delete set null,
  game text not null,
  locale text not null check (locale in ('es', 'pt-BR', 'en')),
  winner_team_id text,
  winner_team_name text,
  team_count integer not null default 0,
  player_count integer not null default 0,
  rounds integer not null default 1,
  results jsonb not null default '{}'::jsonb,
  started_at timestamptz not null default now(),
  completed_at timestamptz not null default now()
);

alter table public.profiles enable row level security;
alter table public.game_sessions enable row level security;

-- No se crean políticas públicas: el acceso inicial pasa exclusivamente por la
-- API de Vercel, que validará el anfitrión o el token individual del jugador.
-- La clave publicable no puede leer ni modificar estas tablas por sí sola.
