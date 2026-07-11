const screen = document.getElementById("screen");
const history = document.getElementById("history");
const promptLine = document.getElementById("promptLine");
const input = document.getElementById("cmdInput");

let typed = "";

const bootMessages = [

"================================================",

"",

"CELESTIA PROBE v1.0",

"",

"Deep Space Autonomous Archive",

"",

"================================================",

"",

"POWER .............. ONLINE",

"Loading navigation systems...",

"Connecting to local vector database...",

"Database connected.",

"NASA index loaded.",

"Wikipedia fallback ready.",

"LANGGRAPH CORE ..... INITIALIZED",

"",

"Awaiting celestial designation...",

""

];
window.onload = async () => {

    input.focus();

    for(const line of bootMessages){

        await systemMessage(line);

        await delay(180);

    }

    renderPrompt();

};

document.body.addEventListener("click", () => input.focus());

document.addEventListener("keydown", () => input.focus());

async function sendQuery(query){

    const response = await fetch(
        "http://127.0.0.1:8000/query",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({query})
        }
    );

    if(!response.ok){

        throw new Error("Backend Error");

    }

    const reader = response.body.getReader();

    const decoder = new TextDecoder();

    let buffer="";

    while(true){

        const {done,value}=await reader.read();

        if(done) break;

        buffer += decoder.decode(value,{stream:true});

        const events = buffer.split("\n\n");

        buffer = events.pop();

        for(const event of events){

            if(!event.startsWith("data:")) continue;

            const data = JSON.parse(event.slice(5));

            console.log(data);

            if(data.type==="progress"){

                await showProgress(data.node);

            }

            if(data.type==="answer"){

                await systemMessage(data.answer);

            }

        }

    }

}
async function showProgress(node){

    switch(node){

        case "planner":

            await systemMessage("Planner Agent ............... COMPLETE");

            break;

        case "archive_check":

            await systemMessage("Archive Check ............... COMPLETE");

            break;

        case "acquisition":

            await systemMessage("Archive Missing");

            await systemMessage("Searching NASA");

            await systemMessage("Downloading article");

            await systemMessage("Chunking documents");

            await systemMessage("Embedding vectors");

            await systemMessage("Writing archive");

            break;

        case "retrieval":

            await systemMessage("Retrieval Agent ............. COMPLETE");

            break;

        case "response":

            await systemMessage("Generating Scientific Report");

            break;

    }

}
function delay(ms){

    return new Promise(resolve=>setTimeout(resolve,ms));

}


function scrollBottom(){

    history.lastElementChild?.scrollIntoView({
    behavior:"smooth",
    block:"end"
});

}


function renderPrompt(){

    promptLine.innerHTML =
        "&gt; " +
        typed +
        '<span class="cursor"></span>';

}


async function systemMessage(text){

    const div = document.createElement("div");

    div.className = "echo";

    history.appendChild(div);

    await typeText(div,text);

    scrollBottom();

}



async function typeText(element,text){

    element.innerHTML="";

    for(const c of text){

        element.innerHTML += c;

        scrollBottom();

        await delay(8);

    }

}
input.addEventListener("keydown", async (e)=>{

    if(e.key==="Backspace"){

        typed=typed.slice(0,-1);

        renderPrompt();

        return;

    }

    if(e.key==="Enter"){

        if(!typed.trim()) return;

        const query=typed.trim();

        const user=document.createElement("div");

        user.className="echo";

        user.textContent="> "+query;

        history.appendChild(user);

        typed="";

        renderPrompt();

        scrollBottom();

    

try{

   await sendQuery(query);

}
catch(error){

    await systemMessage(

`========================================

ERROR

Unable to contact Celestia Archive.

Transmission failed.

========================================`

    );

}

return;

    }

    if(e.key.length===1){

        typed+=e.key;

        renderPrompt();

    }

});

renderPrompt();