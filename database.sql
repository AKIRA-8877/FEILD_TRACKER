BEGIN TRANSACTION;
CREATE TABLE attendance (
	id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	date DATE NOT NULL, 
	check_in DATETIME, 
	check_out DATETIME, 
	status VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id)
);
CREATE TABLE client_visit (
	id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	client_name VARCHAR(100) NOT NULL, 
	company_name VARCHAR(100) NOT NULL, 
	contact_number VARCHAR(20) NOT NULL, 
	location VARCHAR(200) NOT NULL, 
	visit_date DATE NOT NULL, 
	purpose VARCHAR(200) NOT NULL, 
	meeting_notes TEXT, 
	status VARCHAR(20) NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id)
);
CREATE TABLE employee (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	role VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO "employee" VALUES(1,'System Admin','admin@thikse.com','$2b$12$Dj3cDVNl3/X0I5nkgJArIeg0vFsnj5QJmRvqdB10Tvc.xMTgDASGG','admin');
INSERT INTO "employee" VALUES(2,'Test Employee','employee@thikse.com','$2b$12$24hu4j5a.tQDLBnwzivlIuVSVPU88ox7JZqWCslrXClLEDaT9lqfS','employee');
COMMIT;
