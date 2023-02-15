const imgContainer = document.querySelector('.image-container');
const contButton = document.querySelector('.continue-button');

const models = document.querySelectorAll('.model');
const selectModelBtn = document.querySelector('.select-model');

const slideMenu = document.querySelector('.model-selection');
const arrowLogo = document.querySelector('.fa-solid');

const modelInfo = document.querySelector('.model-information');


let file = undefined;
let errorMessage;
let Model = '';


function showFile(input){
	file = input.files[0];
	imgUrl = URL.createObjectURL(file);
	imgContainer.innerHTML = '<img class ="img" src = "'+imgUrl+ '" alt = "user-input-image"/>';
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
    // the firts post to the server

    let options = {method: "POST",
        body: file,
        headers: {'content-type':'img/png'}
        };

    let responseImage = await fetch('/',options);


    options ={method: "POST",
                body: JSON.stringify({'selected model': Model}),
                headers: {'content-type':'application/json'
                 }
                }
    let responseModel  = await fetch('/model',options);

    console.log('model post: ', responseModel);

    options ={method: "POST"}
    let finalResponse = await fetch('/classification',options);
    console.log('final response: ', finalResponse);
}

function postData(){

    let userAuth = userCanProceed();

    if (userAuth){
        
        sendDataToServer();
    }
    else{
        modelInfo.innerText = "Please select a model"
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

// event listeners

contButton.addEventListener('click',(e)=>{
    e.preventDefault();
    postData();

})


models.forEach(model=>{
    model.addEventListener('click', ()=>{
        console.log(model.innerText);
        // define the model to be selected
        Model = model.innerText;
        console.log('variable Model value: ', Model);

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

selectModelBtn.addEventListener('click', ()=>{

    // check if is visible
    let classes = slideMenu.classList;
    // console.log(classes.contains('visible'));
    if(classes.contains('hidden')){
    
        classes.remove('hidden');

        // change the logo to up arrow.
        arrowLogo.classList.remove('fa-chevron-down');
        arrowLogo.classList.add('fa-chevron-up')
    }
    else{


        classes.add('hidden');

        // change the logo to up down.
        arrowLogo.classList.remove('fa-chevron-up');
        arrowLogo.classList.add('fa-chevron-down')
    }
})