console.log('connected');

const BASE_URL = 'http://127.0.0.1:5000/';

const $guessBtn = $('#guess-btn');
const $guessTxt = $('#guess-text');
const guessed = $guessTxt.val();
const $wordsGuessed = $('.guess-history');
const $currScoreView = $('.curr-score')
let currentScore = 0

$guessBtn.on('click', async function(e){
    e.preventDefault();
    const sent_word = await send_guess_to_server($guessTxt.val());
    const status_code = await get_response_from_server(sent_word);
    console.log(status_code);

    if(status_code === 'ok'){
        update_scored_words(sent_word);
        update_score(sent_word);
        console.log('good word');
    } else if (status_code === 'not-on-board'){
        //flash message
        console.log('not on board');
    } else {
        //flash other message
        console.log('invalid word');
    }
    $guessTxt.val('');
    return status_code
})

// send value to server using AXIOS
async function send_guess_to_server(guess){
    const response = await axios({
        method: "POST",
        url: `${BASE_URL}/guess/${guess}`,
        data: guess
      }); 
      return response.config.data;
}

async function get_response_from_server(guess){
    const res = await axios({
        method: "GET",
        url: `${BASE_URL}/guess/${guess}`,
    })

    return res.data;
}

function update_scored_words(guess){
    newLi = `${guess}: ${guess.length}`;
    $wordsGuessed.append(`<li>${newLi}</li>`);
}

function update_score(guess){
    let word_score = guess.length
    currentScore += word_score
    $currScoreView.text(currentScore);
}