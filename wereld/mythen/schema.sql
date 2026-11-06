-- mythen.db: los van de canon. Bron: Wikidata (CC0) + eigen yaml (motieven, clusters, oorsprong, wezens).
create table if not exists entiteit(id text primary key, naam text, naam_nl text, soort text, beschrijving text, bekendheid int, bron text);
create table if not exists kenmerk(entiteit text, kenmerk text, waarde text, unique(entiteit,kenmerk,waarde));
create table if not exists motief(id text primary key, naam text, thompson text, atu text, kern text, kenmerken text);
create table if not exists cluster(id text primary key, naam text, kern text, herkenning text, culturen int, landen int, lokaal int default 0);
create table if not exists lid(cluster text, entiteit text, voorbeeld text, cultuur text, unique(cluster,entiteit,voorbeeld));
create table if not exists oorsprong(cluster text primary key, laag text, canon_codes text, voorstel text, score real, status text, regels text, verlies text, boek text);
create table if not exists vervorming(cluster text, stap int, eeuw text, tekst text, regel text, unique(cluster,stap));
create table if not exists koppel_score(cluster text, canon_code text, score real, treffers text, unique(cluster,canon_code));
