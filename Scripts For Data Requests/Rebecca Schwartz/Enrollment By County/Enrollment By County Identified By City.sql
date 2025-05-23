--(Begin 4)-----------------------------------------------------------------------------------------
SELECT 'All' AS COUNTY,
        COUNT(DISTINCT STUDENT_ID) AS STUDENT_COUNT_2024FA
FROM STUDENT_ENROLLMENT_VIEW AS SEV
WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
AND  (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
AND ENROLL_TERM = '2024FA'
UNION
--(Begin 3)-----------------------------------------------------------------------------------------
SELECT COUNTY,
       COUNT(STUDENT_ID) AS STUDENT_COUNT_2024FA
FROM (
--(Begin 1)-----------------------------------------------------------------
SELECT DISTINCT STUDENT_ID,
                COUNTY,
                ADDRESS_TYPE
      FROM STUDENT_ENROLLMENT_VIEW AS SEV
      JOIN PERSON_ADDRESSES_VIEW AS PAV ON SEV.STUDENT_ID = PAV.ID
        JOIN (VALUES
('Alberton', 'Mineral'),
('Anaconda', 'Deer Lodge'),
('Arlee', 'Lake'),
('Ashland', 'Rosebud'),
('Baker', 'Fallon'),
('Belfry', 'Carbon'),
('Belgrade', 'Gallatin'),
('Belt', 'Cascade'),
('Big Sandy', 'Chouteau'),
('Big Timber', 'Sweet Grass'),
('Bigfork', 'Flathead'),
('Billings', 'Yellowstone'),
('Boulder', 'Jefferson'),
('Bozeman', 'Gallatin'),
('Bridger', 'Carbon'),
('Broadus', 'Powder River'),
('Broadview', 'Yellowstone'),
('Brockton', 'Roosevelt'),
('Browning', 'Glacier'),
('Busby', 'Big Horn'),
('Butte', 'Silver Bow'),
('Cascade', 'Cascade'),
('Charlo', 'Lake'),
('Chester', 'Liberty'),
('Chinook', 'Blaine'),
('Choteau', 'Teton'),
('Circle', 'McCone'),
('Clancy', 'Jefferson'),
('Clyde Park', 'Park'),
('Cohagen', 'Garfield'),
('Colstrip', 'Rosebud'),
('Columbia Falls', 'Flathead'),
('Columbia Fls', 'Flathead'),
('Columbus', 'Stillwater'),
('Conrad', 'Pondera'),
('Corvallis', 'Ravalli'),
('Culbertson', 'Roosevelt'),
('Cut Bank', 'Glacier'),
('Darby', 'Ravalli'),
('Deer Lodge', 'Powell'),
('Denton', 'Fergus'),
('Dillon', 'Beaverhead'),
('Dixon', 'Sanders'),
('Drummond', 'Granite'),
('Dutton', 'Teton'),
('E. Helena', 'Lewis and Clark'),
('East Helena', 'Lewis and Clark'),
('Ekalaka', 'Carter'),
('Ennis', 'Madison'),
('Eureka', 'Lincoln'),
('Fairfield', 'Teton'),
('Fairview', 'Richland'),
('Florence', 'Ravalli'),
('Forsyth', 'Rosebud'),
('Fort Benton', 'Chouteau'),
('Fort Harrison', 'Lewis and Clark'),
('Fort Peck', 'Valley'),
('Frenchtown', 'Missoula'),
('Fromberg', 'Carbon'),
('Geraldine', 'Chouteau'),
('Glasgow', 'Valley'),
('Glendive', 'Dawson'),
('Great Falls', 'Cascade'),
('Hamilton', 'Ravalli'),
('Hardin', 'Big Horn'),
('Harlem', 'Blaine'),
('Harlowton', 'Wheatland'),
('Havre', 'Hill'),
('Hays', 'Blaine'),
('Helena', 'Lewis and Clark'),
('Hot Springs', 'Sanders'),
('Huntley', 'Yellowstone'),
('Huson', 'Missoula'),
('Hysham', 'Treasure'),
('Jefferson City', 'Jefferson'),
('Jefferson Cty', 'Jefferson'),
('Joliet', 'Carbon'),
('Jordan', 'Garfield'),
('Judith Gap', 'Wheatland'),
('Kalispell', 'Flathead'),
('Kalipell', 'Flathead'),
('Laurel', 'Yellowstone'),
('Lewistown', 'Fergus'),
('Libby', 'Lincoln'),
('Livingston', 'Park'),
('Lodge Grass', 'Big Horn'),
('Lolo', 'Missoula'),
('Malta', 'Phillips'),
('Manhattan', 'Gallatin'),
('Marion', 'Flathead'),
('Mc Allister', 'Madison'),
('Miles City', 'Custer'),
('Missoula', 'Missoula'),
('Molt', 'Stillwater'),
('Montana City', 'Jefferson'),
('Nashua', 'Valley'),
('Park City', 'Stillwater'),
('Philipsburg', 'Granite'),
('Pinesdale', 'Ravalli'),
('Plains', 'Sanders'),
('Plentywood', 'Sheridan'),
('Polson', 'Lake'),
('Poplar', 'Roosevelt'),
('Power', 'Teton'),
('Raynesford', 'Judith Basin'),
('Red Lodge', 'Carbon'),
('Roberts', 'Carbon'),
('Ronan', 'Lake'),
('Roundup', 'Musselshell'),
('Ryegate', 'Golden Valley'),
('Scobey', 'Daniels'),
('Seeley Lake', 'Missoula'),
('Shelby', 'Toole'),
('Sheridan', 'Madison'),
('Sidney', 'Richland'),
('Simms', 'Cascade'),
('Somers', 'Flathead'),
('St Ignatius', 'Lake'),
('St. Ignatius', 'Lake'),
('Stanford', 'Judith Basin'),
('Stevensville', 'Ravalli'),
('Stockett', 'Cascade'),
('Sunburst', 'Toole'),
('Superior', 'Mineral'),
('Swan Lake', 'Lake'),
('Terry', 'Prairie'),
('Thompson Falls', 'Sanders'),
('Thompson Fls', 'Sanders'),
('Three Forks', 'Gallatin'),
('Townsend', 'Broadwater'),
('Trout Creek', 'Sanders'),
('Troy', 'Lincoln'),
('Twin Bridges', 'Madison'),
('Ulm', 'Cascade'),
('Valier', 'Pondera'),
('Victor', 'Ravalli'),
('W Yellowstone', 'Gallatin'),
('Walkerville', 'Silver Bow'),
('West Yellowstone', 'Gallatin'),
('White Sulphur Springs', 'Meagher'),
('Whitefish', 'Flathead'),
('Whitehall', 'Jefferson'),
('Wht Sphr Spgs', 'Meagher'),
('Wibaux', 'Wibaux'),
('Winifred', 'Fergus'),
('Wolf Point', 'Roosevelt'),
('Worden', 'Yellowstone')) AS CITY_COUNTY(CITY, COUNTY) ON PAV.CITY = CITY_COUNTY.CITY
      WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
        AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
        AND ENROLL_TERM = '2024FA'
        AND STATE = 'MT'
        AND ADDRESS_TYPE = 'H'
      AND COUNTY IN (
                        'Cascade',
                        'Chouteau',
                        'Glacier',
                        'Lewis and Clark',
                        'Pondera',
                        'Teton',
                        'Toole'
          )
--(End 1)-----------------------------------------------------------------
--(End 2)-----------------------------------------------------------------------------------------
) AS X
GROUP BY COUNTY
--(End 3)-----------------------------------------------------------------------------------------
--(End 4)-----------------------------------------------------------------------------------------