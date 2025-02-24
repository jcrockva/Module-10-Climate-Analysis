# Module-10-Climate-Analysis
Module 10 Climate Analysis


In this module I used the Flask API to connect the hawaii_sqlite data base. This allowed me to retrieve precipitation records, temperature observations, and station details. The database schema is automatically reflected using automap_base().This mapped the Measurement and Station tables to ORM classes for easy querying. A home route was created to access the links for users to access precipitation data, station information, temperature records, and temperature statistics for specified date ranges. The API also was used to create a flexible date-based route, which allows for retrieving minimum, maximum, and average temperatures for a given start date or within a specified date range. These routes use func.min(), func.max(), and func.avg() to compute temperature statistics, ensuring a comprehensive view of historical weather patterns. 

Overall, this API is structured to provide easy access to historical climate data.
