-- Familia en Juego Cloud · anfitriones registrados y estadísticas
-- Supabase Auth debe tener habilitado Email/Password.

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null check (char_length(display_name) between 1 and 60),
  preferred_locale text not null default 'es' check (preferred_locale in ('es', 'pt-BR', 'en')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.rooms
  add column if not exists owner_id uuid references auth.users(id) on delete cascade;

create index if not exists rooms_owner_id_idx on public.rooms(owner_id, created_at desc);

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

create index if not exists game_sessions_owner_idx
  on public.game_sessions(owner_id, completed_at desc);
create index if not exists game_sessions_owner_game_idx
  on public.game_sessions(owner_id, game);

alter table public.profiles enable row level security;
alter table public.game_sessions enable row level security;

-- El backend valida el JWT del anfitrión y accede con la clave secreta.
-- Los clientes no acceden directamente a estas tablas.
