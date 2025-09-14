var express = require('express');
var router = express.Router();
var jsyaml = require("js-yaml");

router.post('/createEvent', function(req, res) {
  let eventDetails;

  eventDetails = jsyaml.safeLoadAll(req.body.eventData, { schema: jsyaml.DEFAULT_FULL_SCHEMA });
  
  createNewEvent(eventDetails);
  
  res.status(200).send({ message: 'Event created successfully' });
});