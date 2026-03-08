async function addVideo(){

const url = document.getElementById("videoUrl").value

if(!url) return

const res = await fetch(`/info?url=${encodeURIComponent(url)}`)
const data = await res.json()

const id = Math.random().toString(36).substring(7)

const container = document.createElement("div")
container.className = "video-item"
container.id = id

container.innerHTML = `
<img src="${data.thumbnail}">
<div>
<p>${data.title}</p>
<button onclick="downloadVideo('${data.url}','${id}')">Download</button>
<div class="progress-bar">
<div class="progress" id="progress-${id}"></div>
</div>
</div>
`

document.getElementById("videoList").appendChild(container)

document.getElementById("videoUrl").value = ""

}


async function downloadVideo(url,id){

const res = await fetch(`/download?url=${encodeURIComponent(url)}`)
const data = await res.json()

const downloadId = data.download_id

checkProgress(downloadId,id,data.file)

}


async function checkProgress(downloadId,id,fileUrl){

const progressBar = document.getElementById(`progress-${id}`)

const interval = setInterval(async ()=>{

const res = await fetch(`/progress?download_id=${downloadId}`)
const data = await res.json()

progressBar.style.width = data.progress + "%"

if(data.progress >= 100){

clearInterval(interval)

const link = document.createElement("a")
link.href = fileUrl
link.click()

}

},1000)

}
