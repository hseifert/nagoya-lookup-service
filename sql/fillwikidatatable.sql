COPY wikidata (country_id,
 	iso_alpha_3_code,
 	iso_alpha_2_code,
 	country_name,
 	alt_name,
    geonames_id,
    region_id,
 	region_name)
FROM '/wikidata_countries.csv'
   WITH CSV
   		DELIMITER ','
   		HEADER
        ;