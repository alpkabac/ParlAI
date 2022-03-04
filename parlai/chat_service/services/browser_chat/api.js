const { spawn } = require('child_process');
const express = require('express');
const app = express();
const { checkPrimeSync } = require('crypto');
const portfinder = require('portfinder');
const uuid = require('uuid');
const bodyParser = require('body-parser');
const NodeCache = require("node-cache");
const { kill, pid } = require('process');
const userCache = new NodeCache();
let python = null;
let pythonPID = null;
let clientID = null;
const userObj = { port: null, pid: null };

app.use(bodyParser.json())

app.post('/open', (req, res) => {

    clientID = req.body.clientID;
    userCache.set(clientID, userObj);
    spawnChild();
    if (spawnChild) {
        const value = userCache.get(clientID);
        res.send({
            status: 'success',
            port: value.port,
            pid: value.pid
        });
    } else {
        res.sendStatus(500);
    }

})

app.post("/status", (req, res) => {

})

app.post("/killprocess", (req, res) => {
    if (clientID != null) {
    const value = userCache.get(clientID);
    if (value.pid != null) {
        try {
            console.log("Killing process with pid:", value.pid);
            process.kill(-value.pid, 'SIGKILL');
            console.log("Ok")
            userCache.del(req.body.clientID);
            res.send({
                status: 'success'
            });
        } catch (e) {
            console.log("Nope")
            res.send({
                error: e
            });
        }
    } else {
        res.send({
            error: "No process found"
        });
        console.log("No process found")
    }
    } else {
        res.send({
            error: "No user found"
        });
        console.log("No user found")
    }
})

function spawnChild() {
    portfinder.getPort(function (err, port) {
        if (err) {
            console.log(err);
        }
        else {
            try {
                python = spawn('python', ['client.py', '--port', '10003', '--serving_port', port, '--host', '0.0.0.0', '--userid', clientID], { detached: true });
                python.stdout.on('data', (data) => {
                    console.log(`stdout: ${data}`);
                });
                python.stderr.on('data', (data) => {
                    console.log(`stderr: ${data}`);
                });
                python.on('close', (code) => {
                    console.log(`child process exited with code ${code}`);
                });
                userObj.port = port;
                userObj.pid = python.pid;
                userCache.set(clientID, userObj);
                value = userCache.get(clientID);
                console.log("Your id is:", clientID, "your port and pid is:", value);
                return true;
            }
            catch (e) {
                console.log(e);
            }
            return false;
        }
    });
}

app.listen(3000, () => {
    console.log('server started on port 3000');
});
