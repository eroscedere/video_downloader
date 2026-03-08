async function addVideo(){

const url = document.getElementById("videoUrl").value

if(!url) return

const res = await fetch(`/info?url=${encodeURIComponent(url)}`)
const data = await res.json()

const container = document.createElement("div")
container.className = "video-item"

container.innerHTML = `
<img src="${data.thumbnail}">
<div>
<p>${data.title}</p>
<button onclick="downloadVideo('${data.url}')">Download</button>
</div>
`

document.getElementById("videoList").appendChild(container)

document.getElementById("videoUrl").value = ""

}

async function downloadVideo(url){

await fetch(`/download?url=${encodeURIComponent(url)}`)

alert("Download iniciado!")

}