import * as helper from "./helper.js";

//Note text editor
const quill = new Quill('#editor', {
  modules: {
    history: {
      delay: 1000,
      maxStack: 500,
      userOnly: true
    },
    toolbar: [
      [{ header: [1, 2, false] }],
      ['bold', 'italic', 'underline'],
    ],
  },
  theme: 'snow', // or 'bubble'
});


helper.initializeApp();


//check for notes currently being viewed in the session
const currentNoteInSession = sessionStorage.getItem("currentNoteViewingName");

//update text editor whether or not a note is currently being viewed
if(currentNoteInSession === null) {
    //write no note selected into the input name 
    const renameInput = document.getElementById("rename-note-input");
    renameInput.value = "No Note Selected";

    //insert an empty delta into the editor to clear the text editor
    const emptyDelta = {
        "ops": [
            { "insert": "Create a note to start saving text" }
        ]
    };

    quill.setContents(emptyDelta);
}else {//note is currently  being viewed
    //display the current note name in the input
    const renameInput = document.getElementById("rename-note-input");
    renameInput.value = sessionStorage.getItem("currentNoteViewingName");

    //display the text from the notes content
    const targetNoteContent = await helper.getNote(currentNoteInSession);

    const delta = JSON.parse(targetNoteContent.content);
    
    quill.setContents(delta);
}

//prevent dialogs from being closed with "Esc"
document.querySelectorAll(".dialog-popup").forEach((dialog) => {
    dialog.addEventListener("keydown", (event) => {
        if (event.key === 'Escape') {
            event.preventDefault();
        }
    })
})


//Listener that reads the search bar input and then prints the notes that are closest to that note searched
document.getElementById("search-bar").addEventListener("input", async (e) => {
    //store the notes grabbed from the api call
    let noteNames = await helper.returnAllNoteNames();
    
    let results = helper.fuzzySearchResult(e.target.value, noteNames);

    //no result after search
    if(results.length === 0){
        helper.clearNoteListUI();

        const noResultElement = document.createElement("h2");
        noResultElement.id = "no-matching-results";

        const nameNode = document.createTextNode("No matching results");

        noResultElement.appendChild(nameNode);
        document.getElementById("scrollable-note-names").appendChild(noResultElement);

    }else{
        helper.clearNoteListUI();
        helper.renderList(results);
    }
})  


//will open a dialog if user wants to DELETE a note or VIEW a note
document.getElementById("scrollable-note-names").addEventListener("click", async (e) => {
    const buttonPressed = e.target.closest("button");

    //prevent user from clicking in the container
    if(buttonPressed === null){
        return;
    }
    
    if(buttonPressed.getAttribute("class") === "note-button") {
        //When a note name button is pressed, that notes name will be put into session storage
        const currentNoteSelectedName = buttonPressed.getAttribute("note");

        //store the current note in session storage
        sessionStorage.setItem("currentNoteViewingName", currentNoteSelectedName);

        //after session storage is set, the value of that note has to be grabbed and sent to the text editor
        const renameInput = document.getElementById("rename-note-input");
        renameInput.value = sessionStorage.getItem("currentNoteViewingName");

        //show contents of the current note in the editor
        const targetNoteContent = await helper.getNote(currentNoteSelectedName);
        const delta = JSON.parse(targetNoteContent.content);
        
        quill.setContents(delta);

    }else if(buttonPressed.getAttribute("class") === "delete-note-button"){
        //change attributes of the dialog to store the target note for deletion
        helper.modifyElementAttribute("delete-note-button",
                                      "data-type",
                                      buttonPressed.getAttribute("target-note") )
        //open dialog
        helper.showDialog("delete-note-dialog");
    }
})


//listeners for all buttons in the close-dialog class to close respective dialog pop-up
document.querySelectorAll(".close-dialog").forEach((button) => {
    button.addEventListener("click", (e) => {
        document.getElementById("create-note-input" ).value = "";
        
        const dialog = button.getAttribute("dialog-id");
        helper.closeDialog(dialog);

        if(dialog === "create-note-dialog"){
            const duplicateNotesMessage = document.querySelector("#create-note-dialog .dialog-body div");

            if(duplicateNotesMessage != null) {
                duplicateNotesMessage.remove();

            }else {
                return;

            }
        }
    }
)
})


//event listener to delete the current note that the user has picked
document.getElementById("delete-note-button").addEventListener("click", async (e) => {
    //Get the data of the note from the current dialog that was opened
    let targetNote = document.getElementById("delete-note-button").getAttribute("data-type"); 

    try{
        await helper.deleteNote(encodeURIComponent(targetNote));
        helper.closeDialog("delete-note-dialog");
        helper.clearNoteListUI();
        
        await helper.refreshNotesUI();

        //if the current note in the session storage is targetNote, it is being viewed in the text editor
        //if so then deleted that note from the session storage
        if(targetNote === sessionStorage.getItem("currentNoteViewingName")) {
            sessionStorage.removeItem("currentNoteViewingName");

            //set renameNoteInput back to empty
            const renameInput = document.getElementById("rename-note-input");
            renameInput.value = "No Note Selected";

            //insert an empty delta into the editor to clear the text editor
            const emptyDelta = {
                "ops": [
                    { "insert": "Create a note to start saving text" }
                ]
            };

            quill.setContents(emptyDelta);
        }
    }catch(error) {
        console.error(error.message);
    }
})


//listener to show create-note dialog
document.getElementById("add-note-button").addEventListener("click", () => {
    helper.showDialog("create-note-dialog");
})


//event listener to create a new note
document.getElementById("create-note-button").addEventListener("click", async (e) => {
    //get the current text that was written in the dialog text input
    let input = helper.getTextElementInput("create-note-input");

    //Prevent note creation from empty note names
    if(input.length === 0) {
        return;
    }else if(helper.isAllSpaces(input) === true) {
        return;
    }

    const doNotesExist = await helper.doNotesExist(); //true if note exists false if none

    //api call which returns true or false for correct running
    let noteInputReturn = await helper.createNote(input);


    if(noteInputReturn === false) {//name of the note trying to be created already exists

        //show an error on the dialog by inserting an html element saying that this note already exists
        const noteExistsErrorMessage = document.querySelector("#create-note-dialog .dialog-body div");

        if(noteExistsErrorMessage === null) {
            let container = document.querySelector("#create-note-dialog .dialog-body");
            const errorMessage = document.createElement("div");
            errorMessage.textContent = "Note name already exists"

            container.appendChild(errorMessage);
        }else {
            return;
        }

    }else {//note created has a unique name

        if(!doNotesExist) {//no notes currently exist. database is empty
            //close the dialog page
            helper.closeDialog("create-note-dialog");

            //clear the "No Notes" message from the notes sliding page
            const noNotesMessage = document.querySelector("#scrollable-note-names h1");
            noNotesMessage.remove()

            //render the list with the new note created
            let listOfNotes = await helper.returnAllNoteNames();
            helper.renderList(listOfNotes);

            //clear the text input
            document.getElementById("create-note-input" ).value = "";
 
        }else {//one or more notes exist
            
            helper.closeDialog("create-note-dialog");
            helper.clearNoteListUI();

            await helper.refreshNotesUI();

            //clear the text input
            document.getElementById("create-note-input" ).value = "";
        }

        //Remove the duplicate notes error message if it exists
        const duplicateNotesMessage = document.querySelector("#create-note-dialog .dialog-body div");

        if(duplicateNotesMessage != null) {
            duplicateNotesMessage.remove();
        }

        //set the name of the note after creation
        const renameInput = document.getElementById("rename-note-input");
        renameInput.value = input;

        //set the new note for the session storage
        sessionStorage.setItem("currentNoteViewingName", input);

        //create a delta and set the currentContent to that delta
        const emptyDelta = {
            "ops": [
                { "insert": "\u200B" }
            ]
        };

        quill.setContents(emptyDelta);
    }
})























//text input to rename a note
document.getElementById("rename-note-input").addEventListener("focusout", async (e) => {
    //check whether there is a note in session storage
    if(sessionStorage.getItem("currentNoteViewingName") == null) {
        const renameInput = document.getElementById("rename-note-input");
        renameInput.value = "No Note Selected";
        
        return;
    }
    
    //rename note input
    const newNameInput = e.target.value;

    //modal popups
    const emptyNoteNameDialog = document.getElementById("rename-note-empty-dialog");
    const duplicateNoteNameDialog = document.getElementById("rename-note-duplicate-dialog")
    
    //current name is nothing, no changes are made, a name is required
    if(newNameInput.length == 0) {
        emptyNoteNameDialog.showModal();
        return;
    }

    //The rename is the same as what was before, no changes are made
    if(newNameInput == sessionStorage.getItem("currentNoteViewingName")) {
        return;
    }

    //The name is a duplicate and the current name already exists, either true or false
    const didRenameNoteWork = await helper.renameNote(sessionStorage.getItem("currentNoteViewingName"), newNameInput);
    
    //change the current note name in session storage, refresh the ui
    if(didRenameNoteWork) {        
        sessionStorage.setItem("currentNoteViewingName", newNameInput)
        helper.clearNoteListUI();
        helper.refreshNotesUI();
    }else {
        duplicateNoteNameDialog.showModal();

        const renameInput = document.getElementById("rename-note-input");
        renameInput.value = sessionStorage.getItem("currentNoteViewingName");
    }
})


let timer;

//autosave when user typing stops
quill.on('text-change', () => {
    clearTimeout(timer);
    timer = setTimeout(() => {

        const delta = quill.getContents();
        const jsonDelta = JSON.stringify(delta);
        const currentNoteInSession = sessionStorage.getItem("currentNoteViewingName")

        //check whether a note has been selected
        if(currentNoteInSession == null) {//if there is no note in session, do nothing
            return;
        }else {//a note is currently in session and needs to be updated
            //send the jsonDelta to the api
            helper.modifyNoteContent(sessionStorage.getItem("currentNoteViewingName"), jsonDelta);
        }

    }, 500);
});

//autosave every 10 seconds
quill.on('text-change', helper.throttle(() => {
    const delta = quill.getContents();
    const jsonDelta = JSON.stringify(delta);
    const currentNoteInSession = sessionStorage.getItem("currentNoteViewingName")

    //check whether a note has been selected
    if(currentNoteInSession == null) {//if there is no note in session, do nothing
        return;
    }else {//a note is currently in session and needs to be updated

        //send the jsonDelta to the api
        helper.modifyNoteContent(sessionStorage.getItem("currentNoteViewingName"), jsonDelta);
    }

    //refresh the ui to show modified date
    helper.clearNoteListUI();
    helper.refreshNotesUI();
}, 10000));

//to-do
//when a note is selected the button of the note will change color making it easier for the user to know what button was clicked