// let accepts = require('accepts');
// let escape = require('escape-html');
// let mime = require('send').mime;
// var app = require('express')();

// app.post('/submit', (req, res) => {
//     const {
//         body: { id, challengeType, solution, githubLink }
//     } = req;

//     if (!ObjectID.isValid(id)) {
//         log('isObjectId', id, ObjectID.isValid(id));
//         return res.status(403).send(`The provided ID: ${id} is not a valid submission.`);
//     }
//     if ('challengeType' in req.body && !isNumeric(String(challengeType))) {
//         log('challengeType', challengeType, isNumeric(challengeType));
//         return res.status(403).json({
//             type: 'error',
//             message: 'That does not appear to be a valid challenge submission.'
//         });
//     }
// });   

let accepts = require('accepts');
let escape = require('escape-html');
let mime = require('send').mime;
measureServer = require('express')();

measureServer.post(PATH, (req, res) => {
    const { method, endpoint, response } = req.body;

    createMockRoute(method, endpoint, response);

    // sends a sanitized confirmation back that the route has been created
    res.send(`Measure route to ${endpoint} has been created.`);
});