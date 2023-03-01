const imgContainer = document.querySelector('.image-container');
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
	file = input.files[0];
	imgUrl = URL.createObjectURL(file);
	imgContainer.innerHTML = '<img class ="img" src = "'+imgUrl+ '" alt = "user-input-image"/>';
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
    // the firts post to the serve
    let options = {method: "POST",
        body: file,
        headers: {'content-type':'img/png'}
        };

    // show backdrop
        showBackdrop();

    let responseImage = await fetch('/',options);

    options ={method: "POST",
                body: JSON.stringify({'selected model': Model}),
                headers: {'content-type':'application/json'
                 }
                }
    let responseModel  = await fetch('/model',options);
    options ={method: "POST"}
    let finalResponse = await fetch('/classification',options);
    finalResponse = await finalResponse.json();

    // hide backdrop
    hideBackdrop();
    showResults(finalResponse);

    console.log('final response: ', finalResponse);
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
    let resultDiv = '<div class="result-info p-3"><div class="result-title"><h3> RESULTS</h3></div><div class="top5-container"><div class="indexes"><ol class="top5-categories"><li>1st</li><li>2nd</li><li>3rd</li><li>4th</li><li>5th</li></ol></div><div class="categories"><ol class="top5-categories"><li>' + resultsObject.categories[0] + '</li><li>' + resultsObject.categories[1] + '</li><li>' + resultsObject.categories[2] + '</li><li>' + resultsObject.categories[3] + '</li><li>' + resultsObject.categories[4] + '</li></ol></div><div class="probabilities"><ol class="top5-probabilities"><li>'+ resultsObject.probabilities[0].toFixed(2) + '% </li><li>' + resultsObject.probabilities[1].toFixed(2) + ' % </li><li>' + resultsObject.probabilities[2].toFixed(2) + ' % </li><li>' + resultsObject.probabilities[3].toFixed(2) + ' % </li><li> ' + resultsObject.probabilities[4].toFixed(2) + ' % </li></ol></div></div></div>'
    
    let mainContainerDiv = document.querySelector('.main-container');
    let resultInfo = document.querySelector('.result-info');

    if (resultInfo){
        mainContainerDiv.removeChild(mainContainerDiv.children[4])//remove the 4th child
    }
    
    mainContainerDiv.innerHTML += resultDiv;
    }

// event listeners

contButton.addEventListener('click',(e)=>{
    e.preventDefault();
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

// capturing  image from user camera

function hasGetUserMedia() {
    return !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

async function captureImage(){
    let stream;//define an initial stream

    let constraints = {
        audio: false,
        video: true,
    }

    try{
        stream  = await navigator.mediaDevices.getUserMedia(constraints);
        // https://web.dev/getusermedia-intro/
        console.log(stream);
        // TODO: need to process the stream of data show on screem and allow user to take a pic.

    } catch (err){
        alert(err);
    }
}

cameraIcon.addEventListener('click', ()=>{
    captureImage();
});


// TODO: ADD THE FUNC TO ADD NEW IMAGE