current_stage = 0
stages = []
var i = 0;
var running;

function runbar() {
        if (i == 0) {
                i = 1;
                var elem = document.getElementById("myBar");
                var width = 1;
                running = setInterval(() => {
                        if (width >= 98) {
                                clearInterval(running);
                                i = 0;
                        } else {
                                width++;
                                elem.style.width = width + "%";
                        }
                }, 35);
        }
}

function enable_send_button() {
        document.getElementById("send").onclick = () => {
                document.getElementById("send").onclick = undefined
                next_stage("Initializing Process...");
        };
}

function process_ended(msg) {
        clearInterval(running);
        //document.getElementById("myBar").style.width = "100%";
        current_stage = 0;
        document.getElementById("msg").textContent = msg
        enable_send_button()
}

function process_failed(msg) {
        console.log("failed at stage " + current_stage)
        clearInterval(running);
        document.getElementById("myBar").style["background-color"] = "red"
        document.getElementById("msg").textContent = msg
        current_stage = 0
        i = 0
        enable_send_button()
}

async function next_stage(msg) {
        document.getElementById("myBar").style["background-color"] = "green"
        document.getElementById("msg").textContent = msg
        runbar()
        await stages[current_stage]()
        current_stage += 1
}

async function stage1() {
        await new Promise(resolve => setTimeout(resolve, 1500));
        const request =  await fetch('/stage1.php', {
                method: 'POST',
                body: "level=Stage 1",
                headers: {"Content-Type" : "application/x-www-form-urlencoded"}
        }).then((response) => {
                response.json().then((data) => {
                        if (data.status == "success") {
                                next_stage(data.message)
                        } else {
                                process_failed(data.message)
                        }
                })
        })
}

async function stage2() {
        await new Promise(resolve => setTimeout(resolve, 1500));
        boundary = "-----------------------------52420834717669863042164438696"
        returnline = "\r\n"
        data = boundary + returnline
        data += "Content-Disposition: form-data; name=\"level\"" + returnline
        data += returnline
        data += "Stage 2" + returnline
        data += "-----------------------------52420834717668863042164438696" + returnline
        data += "Content-Disposition: form-data; name=\"random\"" + returnline
        data += returnline
        data += boundary.substr(33, 43) + returnline
        data += "-----------------------------52420834717669863042164438696--"
        
        const request =  await fetch('/stage2.php', {
                method: 'POST',
                headers: {
                        "Content-Type": "multipart\\form-data; boundary=--------------------------52420834717669863042164438696"
                },
                body: data
        }).then((response) => {
                response.json().then((data) => {
                        if (data.status == "success") {
                                next_stage(data.message)
                        } else {
                                process_failed(data.message)
                        }
                })
        })
}

async function stage3() {
        await new Promise(resolve => setTimeout(resolve, 1500));
        const request =  await fetch('/stage3.php', {
                method: 'POST',
                body: "level=Stage 3",
                headers: {"Content-Type" : "application/x-www-form-urlencoded"}
        }).then((response) => {
                response.json().then((data) => {
                        if (data.status == "success") {
                                process_ended(data.message)
                        } else {
                                process_failed(data.message)
                        }
                })
        })
}

stages = [stage1, stage2, stage3]

document.addEventListener('DOMContentLoaded', () => {
        enable_send_button()
});