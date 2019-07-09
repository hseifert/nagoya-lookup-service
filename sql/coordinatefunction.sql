

/*below query will output countrynames and NP party status of all countries within the input radius of the queried coordinates--
SELECT n.party, geo.countryname
FROM nagoya n 
INNER JOIN geonames geo ON n.code = geo.iso2
INNER JOIN eezlandunion e ON geo.iso3 = e.iso_3digit
WHERE ST_DWithin(geom,
             ST_transform(
    	          ST_geomfromtext('POINT(-11.206339 51.077239)', 4326), 4326), 0.1);
                  
--OR this function can be used, it works the same, has the same output--
--be aware 0.1 as radius is equal to 100m--

SELECT n.party, geo.countryname
FROM nagoya n 
INNER JOIN geonames geo ON n.code = geo.iso2
INNER JOIN eezlandunion e ON geo.iso3 = e.iso_3digit
WHERE ST_DWithin(geom, ST_SetSRID(ST_MakePoint(-11.206339, 51.077239), 4326), 0.1);*/

drop function if exists nplookup;
--------------------------------------------------------------------------------------
    
--make this a function for convenience--
CREATE OR REPLACE FUNCTION nplookup (coords varchar(255), radius int)
RETURNS TABLE (nagoya_iso2 varchar (2), party_date date, marine_regions_country varchar (100), wikidata_country text, distance numeric)
AS $$
BEGIN
    RETURN QUERY
    SELECT n.code, n.party, e.country, w.country_name, round(ST_Distance(e.geom::geography,st_geographyfromtext(concat('POINT(' , coords, ')')))::numeric, 0) AS distance
    FROM eezlandunion e
    		LEFT JOIN geonames geo ON geo.iso3 = e.iso_3digit
			LEFT JOIN wikidata w	ON geo.geonameid = w.geonames_id
 										OR (e.country = w.country_name)
 										OR (w.region_name = e.country)
										OR (w.alt_name = e.country AND e.iso_3digit = w.iso_alpha_3_code) 
                           	 			OR (e.iso_3digit = w.iso_alpha_3_code)
			LEFT JOIN nagoya n  ON n.code = geo.iso2 
									OR n.code = w.iso_alpha_2_code
    WHERE ST_DWithin(e.geom::geography,
    	          st_geographyfromtext(concat('POINT(' , coords, ')')), radius)
    GROUP BY n.code, n.party, e.country, w.country_name, e.geom              
    ORDER BY ST_Distance(e.geom::geography,st_geographyfromtext(concat('POINT(' , coords, ')')));
	
END
$$ LANGUAGE plpgsql;

--finished lookupfunction which returns country and party status of coords--
--be aware that the radius unit is meters--
-- coordinates to be enteres as longitude, latitude in signed degrees format with 8 significant digits--
select * from nplookup('-5.825922 51.968407', 8000);