// Run this script using:
// mongo < init_mongo.js

// use iot

db.createCollection("sensor")

db.sensor.insertOne({
  temperature: 25.4,
  humidity: 58.9,
  timestamp: new Date()
})
