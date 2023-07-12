// const imgContainer = document.querySelector('.image-container');
const contButton = document.querySelector('.continue-button');

const models = document.querySelectorAll('.model');
const selectModelBtn = document.querySelector('.select-model');

const slideMenu = document.querySelector('.model-selection');
const arrowLogo = document.querySelector('.fa-solid');

const modelInfo = document.querySelector('.model-information');
const cameraIcon = document.querySelector('.camera-icon');


let file = undefined;
let errorMessage;
let Model = '';

function showFile(input){
    // define o valor de file, uma variavel global que armazena o arquivo selecionado.
    console.log(input.files)
	let fileUploaded = input.files[0];
	imgUrl = URL.createObjectURL(fileUploaded);
    const imgContainer = document.querySelector('.image-container');
	imgContainer.innerHTML = '<img class ="img" src = "'+imgUrl+ '" alt = "user-input-image"/>';

    // ṿerify if already have a result div. If yes, remove it.
    let mainContainerDiv = document.querySelector('.main-container');
    let resultInfo = document.querySelector('.result-info');

    if (resultInfo){
        mainContainerDiv.removeChild(resultInfo)//remove the 4th child
    }

    // salvar o arquivo como dataUrl:
    const fileReader = new FileReader();
    fileReader.addEventListener('load', (event)=>{
        const result = event.target.result;
        console.log({result})
        // assign the base64 data to the global variable file
        file = result;
    })

    fileReader.readAsDataURL(fileUploaded);
}

function hideBackdrop(){
    const backdrop = document.querySelector('.backdrop');
    const loader = document.querySelector('.loader');
    backdrop.classList.add('off');
    backdrop.classList.remove('on');

    loader.classList.add('off');
    loader.classList.remove('on');
}

function showBackdrop() {
    const backdrop = document.querySelector('.backdrop');
    const loader = document.querySelector('.loader');
    backdrop.classList.add('on');
    loader.classList.add('on');

    backdrop.classList.remove('off');
    loader.classList.remove('off');
}

function userCanProceed(){
    if (!Model){
        errorMessage = 'Please select a Classification Model';
        return false;
    }

    if (file==undefined){
        errorMessage =  'Please select an image from your computer. '
        return false;
    }
    return true;
}


async function sendDataToServer(){

    let [dataType,image64Code] = file.split(',');
    dataType = dataType.split(';')[0].split(':')[1]
    console.log({dataType,image64Code});

    let requestBody = {
        rawData: file,
        dataType: dataType,
        image64Code: image64Code,
        model: Model
    };

    // the firts post to the serve
    let options = {method: "POST",
        body: JSON.stringify(requestBody),
        headers: {'content-type':'application/json'}
        };

    console.log({requestBody});
    console.log({options});

    // // show backdrop
    showBackdrop();

    let serverClassResponse = await fetch('/classification',options);
    let finalResponse = await serverClassResponse.json()
    finalResponse = JSON.parse(finalResponse)
    hideBackdrop();
    showResults(finalResponse);

    // console.log('final response: ', finalResponse);
}

function postData(){

    let userAuth = userCanProceed();

    if (userAuth){
        
        sendDataToServer();
    }
    else{
        modelInfo.innerText = "Please select a model and upload an image"
        modelInfo.classList.add('Error');
    }
}

function sendData(data){
    const formData = new FormData();

    for(const name in data){
        formData.append(name, data[name]);
    }
    let options = {
    method: "POST",
    body: formData
    }
    let r = fetch('/',options);
    r.then(res=>console.log(res));

}

function showResults(resultsObject){

    let divResults = document.createElement('div');
    divResults.classList.add('result-info');
    divResults.classList.add('p-3');
    divResults.innerHTML = `
    <div class="result-title">
        <h3> RESULTS</h3>
    </div>
    <div class="top5-container">
        <div class="indexes">
            <ol class="top5-categories">
                <li>1st</li>
                <li>2nd</li>
                <li>3rd</li>
                <li>4th</li>
                <li>5th</li>
            </ol>
        </div>
        <div class="categories">
            <ol class="top5-categories">
                <li>${resultsObject.categories[0]}</li>
                <li>${resultsObject.categories[1]}</li>
                <li>${resultsObject.categories[2]}</li>
                <li>${resultsObject.categories[3]}</li>
                <li>${resultsObject.categories[4]}</li>
            </ol>
        </div>
        <div class="probabilities">
            <ol class="top5-probabilities">
                <li>${resultsObject.probabilities[0].toFixed(2)}%</li>
                <li>${resultsObject.probabilities[1].toFixed(2)}% </li>
                <li>${resultsObject.probabilities[2].toFixed(2)}%</li>
                <li>${resultsObject.probabilities[3].toFixed(2)}% </li>
                <li>${resultsObject.probabilities[4].toFixed(2)}% </li>
            </ol>
        </div>
    </div>`;

    let mainContainerDiv = document.querySelector('.main-container');
    mainContainerDiv.appendChild(divResults);
    }

// capturing  image from user camera

function hasGetUserMedia() {
    return !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

async function captureImage(videoElement){

    let constraints = {
        audio: false,
        video: true,
    }

    console.log(videoElement);

    try{
        console.log(navigator.mediaDevices.enumerateDevices());

        let mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        videoElement.srcObject = mediaStream;
        videoElement.onloadedmetadata = (e)=>{
            console.log('Pronto')
            // adicionar um evento clique para todo o overlay e capturar a imagem.
        };

        console.log(mediaStream);

        // let track = mediaStream.getAudioTracks()[0];

        return mediaStream;


        // 

        // navigator.mediaDevices.getUserMedia(constraints, (dataStream)=>{
        //     videoElement.src = window.URL.createObjectURL(dataStream);


        //     videoElement.onloadedmetadata = (e)=>{
        //         console.log('Pronto');
        //     }
        // }, (err)=> alert(`Erro ao acessar a camera: ${err}`));

        // https://web.dev/getusermedia-intro/
        // console.log(stream);
        // TODO: need to process the stream of data show on screem and allow user to take a pic.

    } catch (err){
        alert(err);
    }
}

// event listeners

contButton.addEventListener('click',(e)=>{
    // e.preventDefault();
    console.log('clicado');
    postData();

})

models.forEach(model=>{
    model.addEventListener('click', ()=>{
 
        // define the model to be selected
        Model = model.innerText;

        modelInfo.innerText = 'The model selected is ' + Model;
        let listaClasses = modelInfo.classList;
        if(listaClasses.contains('Error')){
            modelInfo.classList.remove('Error');
        }

       
        // remove the selected class from others and add only on the clicked button.
        models.forEach(modelo=>{
            if(modelo.classList.contains('selected')){
                modelo.classList.remove('selected');
            } 
        })
        
         // change the syle, to indicate the selection.
        model.classList.add('selected');

        })
})

function showOrHideMenu(){
    let classes = slideMenu.classList;
    // console.log(classes.contains('visible'));
    if(classes.contains('menu-hidden')){
    
        classes.remove('menu-hidden');

        // change the logo to up arrow.
        arrowLogo.classList.remove('fa-chevron-down');
        arrowLogo.classList.add('fa-chevron-up')

    }
    else if(!classes.contains('menu-hidden')){
        console.log('event invoqued');
        classes.add('menu-hidden');
        // change the logo to up down.
        arrowLogo.classList.remove('fa-chevron-up');
        arrowLogo.classList.add('fa-chevron-down')
    }
}

selectModelBtn.addEventListener('click',  e=>{
    e.stopPropagation();
    showOrHideMenu();
});

const infoShow = document.querySelector('.what-is-it');
const infoBanner = document.querySelector('.info-banner');
let infoClassList = infoBanner.classList;

infoShow.addEventListener('click', ()=>{

    if (infoClassList.contains('not-show')){
        infoClassList.remove('not-show');
        infoClassList.add('shown');        
    }
    else{
        infoClassList.remove('shown');
        infoClassList.add('not-show');
    }

})

const body = document.body;
body.addEventListener('click', (e)=>{
    let target = e.target;

    if(target.classList.contains('select-model')){
        return null;
    }
    else{

        if (infoClassList.contains('shown')){
             infoClassList.remove('shown');
            infoClassList.add('not-show'); 
        }

        if ( ! slideMenu.classList.contains('menu-hidden')){
            showOrHideMenu();
        }
        console.log('body event');

    }

} ,{capture: true})



cameraIcon.addEventListener('click', async ()=>{

    // mostrar o overlay da camera
    let captureOverlay = document.querySelector('.video-overlay');
    let fecharBtn = document.querySelector('.close-capture');
    let videoElement = document.querySelector('.video-capture');
    
    captureOverlay.classList.remove('hidden');

    let mediaStream = await captureImage(videoElement);
    let track = mediaStream.getVideoTracks()[0];

    let capture = new ImageCapture(track);
    console.log(capture);



});


// pegando camera do usuario:
    // ao clicar na camera, mostrar um overlay.
    // esse overlay possui um div central, com um elemento <video></video>
    // video.src precisa receber o datastream do metodo getUserMedia.

// adicionar suporte para mais de um  modelo.

/*
-estilizar video overlay e container
-ao clicar da camera, mostrar o overlay
-transmitir a stream do video para o elemento de video.
-ao fechar precisa eliminar isso.
*/