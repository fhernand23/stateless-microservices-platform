// Definitions
var dbUser = 'cdb_app_user';
var dbPwd = 'cdb_app_pass';
var dbName = 'theDb';

// create database
db = db.getSiblingDB(dbName);

// Create the default database with and user
db.createUser(
    {
        user: "cdb-adm-user",
        pwd: "cdb-adm-pass",
        roles: [
            {
                role: "readWrite",
                db: "app0db"
            }
        ]
    }
);


// Create collections
db.createCollection('base.user');
