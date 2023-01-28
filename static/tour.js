// const room = "room.jpg"
const Entrance = new PANOLENS.ImagePanorama("room.jpg");
const viewer1 = new PANOLENS.Viewer({
container: document.querySelector("#Entrance")
});
viewer1.add(Entrance);

const Campus = new PANOLENS.ImagePanorama("vjti.jpeg");
const viewer2 = new PANOLENS.Viewer({
container: document.querySelector("#Campus")
});
viewer2.add(Campus);

const Room = new PANOLENS.ImagePanorama("room.jpg");
const viewer3 = new PANOLENS.Viewer({
container: document.querySelector("#Room")
});
viewer3.add(Room);

const Lib = new PANOLENS.ImagePanorama("room.jpg");
const viewer4 = new PANOLENS.Viewer({
container: document.querySelector("#Lib")
});
viewer4.add(Lib);