const College1 = new PANOLENS.ImagePanorama("static/images/dj_entrance.jpg");
const viewer1 = new PANOLENS.Viewer({
container: document.querySelector("#College1")
});
viewer1.add(College1);

const College2 = new PANOLENS.ImagePanorama("static/images/vjti_entrance.jpg");
const viewer2 = new PANOLENS.Viewer({
container: document.querySelector("#College2")
});
viewer2.add(College2);

const College3 = new PANOLENS.ImagePanorama("static/images/dj_canteen.jpg");
const viewer3 = new PANOLENS.Viewer({
container: document.querySelector("#College3")
});
viewer3.add(College3);