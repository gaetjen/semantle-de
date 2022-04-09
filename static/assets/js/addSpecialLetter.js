function addLetter(l) {
    let guessBox = document.getElementById("guess");
    guessBox.value += l;
    guessBox.focus();
}