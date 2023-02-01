// const room = "room.jpg"]

/**
 * 
 * onLoad event 
 * createElement 
 */

// import axios from 'axios'

let req_options = {
    url: '/fetch_cllg',
    method: "GET",

}

let response = await axios.request(req_options)
// var cllg_data;
// axios.get('/fetch_cllg')
//   .then(function (response) {
//     // handle success
//     //   console.log(response);
//       cllg_data = response.data;
//     //   console.log(cllg_data.length)
//   })
//   .catch(function (error) {
//     // handle error
//     console.log(error);
//   })

// console.log(response)
  var cllg_data = response.data

// for (var i = 0; i < response.length; i++){
//     console.log(i)
// }
// console.log(cllg_data)

var url = window.location.href.split('/')

var cllg1=url[4]

var cllg;
// cllg_data?.map((cllg) => {
//     // console.log(cllg.description)
//     if (cllg.description == cllg1) {
//         var image1 = cllg.filename;
//         var image2 = cllg.classroom;
//         var image3 = cllg.library;
//         var image4 = cllg.canteen;
        
//     }
    
// })
if (cllg_data) {
    for (var i = 0; i < cllg_data.length; i++) {
        console.log(cllg_data[i])
        // console.log(cllg_data[i]._id.$oid);
        // console.log(cllg1)
        if (cllg_data[i]._id.$oid== cllg1) {
            var image1 = cllg_data[i].filename;
            var image2 = cllg_data[i].classroom;
            var image3 = cllg_data[i].library;
            var image4 = cllg_data[i].canteen;
            var text = cllg_data[i].voice;
            document.getElementById("College_name").innerHTML = cllg_data[i].description
            // console.log(image1)
            break;
        }
    }
}

function dexter_voice(){
    function getVoices() {
       let voices = speechSynthesis.getVoices();
       if(!voices.length){
         // some time the voice will not be initialized so we can call spaek with empty string
         // this will initialize the voices 
         let utterance = new SpeechSynthesisUtterance("");
         speechSynthesis.speak(utterance);
         voices = speechSynthesis.getVoices();
       }
       return voices;
     }
     
     
     function speak(text, voice, rate, pitch, volume, lang) {
       // create a SpeechSynthesisUtterance to configure the how text to be spoken 
       let speakData = new SpeechSynthesisUtterance();
       speakData.volume = volume; // From 0 to 1
       speakData.rate = rate; // From 0.1 to 10
       speakData.pitch = pitch; // From 0 to 2
       speakData.text = text;
       speakData.lang = lang;
       speakData.voice = voice;
       
       // pass the SpeechSynthesisUtterance to speechSynthesis.speak to start speaking 
       speechSynthesis.speak(speakData);
     
     }
    
     if ('speechSynthesis' in window) {
    
       let voices = getVoices();
       let rate = 1, pitch = 1, volume = 1;
      
     
        //  speak(text, voices[5], rate, pitch, volume, 'hi-IN');
         speak(text, voices[5], rate, pitch, volume, 'en');
     //   for(i=0; i<voices.length; i++){
     //     console.log(voices[i])
     //   }
     //   console.log(voices[5])
     }else{
       console.log(' Speech Synthesis Not Supported 😞'); 
     }
 }
 dexter_voice();


//   console.log(cllg_data[1])
const Entrance = new PANOLENS.ImagePanorama("/static/uploads/"+image1);
const viewer1 = new PANOLENS.Viewer({
container: document.querySelector("#Entrance")
});
viewer1.add(Entrance);

const Campus = new PANOLENS.ImagePanorama("/static/classroom/"+image2);
const viewer2 = new PANOLENS.Viewer({
container: document.querySelector("#Campus")
});
viewer2.add(Campus);

const Room = new PANOLENS.ImagePanorama("/static/library/"+image3);
const viewer3 = new PANOLENS.Viewer({
container: document.querySelector("#Room")
});
viewer3.add(Room);

const Lib = new PANOLENS.ImagePanorama("/static/canteen/"+image4);
const viewer4 = new PANOLENS.Viewer({
container: document.querySelector("#Lib")
});
viewer4.add(Lib);