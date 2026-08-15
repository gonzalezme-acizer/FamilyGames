-- Familia en Juego Cloud · salas y contenido multidioma
-- Ejecutar una sola vez después de schema.sql.

alter table public.rooms
  add column if not exists locale text not null default 'es'
  check (locale in ('es', 'pt-BR', 'en'));

alter table public.content_cards
  add column if not exists content_key text,
  add column if not exists source_locale text not null default 'es'
  check (source_locale in ('es', 'pt-BR', 'en'));

update public.content_cards
set content_key = encode(digest(game || ':' || id::text, 'sha256'), 'hex')
where content_key is null;

alter table public.content_cards alter column content_key set not null;
create unique index if not exists content_cards_content_key_idx
  on public.content_cards(content_key);

create table if not exists public.content_card_translations (
  card_id uuid not null references public.content_cards(id) on delete cascade,
  locale text not null check (locale in ('es', 'pt-BR', 'en')),
  category text,
  payload jsonb not null,
  reviewed boolean not null default false,
  updated_at timestamptz not null default now(),
  primary key (card_id, locale)
);

insert into public.content_card_translations(card_id, locale, category, payload, reviewed)
select id, 'es', category, payload, true
from public.content_cards
on conflict (card_id, locale) do nothing;

create index if not exists content_card_translations_locale_idx
  on public.content_card_translations(locale, card_id);

alter table public.content_card_translations enable row level security;

comment on column public.rooms.locale is 'Idioma compartido por tablero, TV y celulares de la sala';
comment on column public.content_cards.content_key is 'Identificador estable para importar y actualizar sin duplicados';
comment on column public.content_card_translations.reviewed is 'La traducción fue revisada para uso familiar';
