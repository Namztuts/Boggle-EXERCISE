class BoggleGame {
   /* make a new game at this DOM id */
   constructor(boardId, secs = 60) {
      this.secs = secs; // game length
      this.showTimer();

      this.score = 0;
      this.words = new Set();
      this.board = $('#' + boardId);

      // every 1 second (1000 msec), "tick"
      this.timer = setInterval(this.tick.bind(this), 1000);

      $('.add-word', this.board).on('submit', this.handleSubmit.bind(this));
   }

   /* show word in list of words */
   showWord(word) {
      $('.words', this.board).append($('<li>', { text: word })); //selecting the ul in HTML | second param is selecting ONLY if it is within the board (#boardID)
   } //____________________________________________________________'text' is referencing/setting the HTML attribute | 'word' is the user input

   /* show score in html */
   showScore() {
      $('.score', this.board).text(this.score);
   }

   /* show a status message */
   showMessage(msg, cls) {
      $('.msg', this.board).text(msg).removeClass().addClass(`msg ${cls}`);
   }

   /* handle submission of word: if unique and valid, score & show */
   async handleSubmit(evt) {
      evt.preventDefault();
      console.log(this);
      const $word = $('.word', this.board);

      let word = $word.val();
      if (!word) return;

      if (this.words.has(word)) {
         //if the dictionary (words.txt) has the word in it
         this.showMessage(`Already found ${word}`, 'err');
         return;
      }

      // check server for validity
      const resp = await axios.get('/check-word', { params: { word: word } }); //going to check-word route in Python | Object for parameters | https://site.com/get?word=word
      console.log('response ==>', resp);
      console.log('data ==>', resp.data);
      console.log('result ==>', resp.data.result);

      if (resp.data.result === 'not-word') {
         this.showMessage(`${word} is not a valid English word!`, 'err');
      } else if (resp.data.result === 'not-on-board') {
         this.showMessage(
            `${word} is not a valid word within this board!`,
            'err'
         );
      } else {
         this.showWord(word);
         this.score += word.length;
         this.showScore();
         this.words.add(word);
         this.showMessage(`Added: ${word}`, 'ok');
      }

      $word.val('').focus(); //focus back onto the input field
   }

   /* Update timer in DOM */
   showTimer() {
      $('.timer', this.board).text(this.secs);
   }

   /* Tick: handle a second passing in game */
   async tick() {
      this.secs -= 1;
      this.showTimer();

      if (this.secs === 0) {
         clearInterval(this.timer);
         await this.scoreGame();
      }
   }

   /* end of game: score and update message. */
   async scoreGame() {
      // sending to /post-score | axios POST requests send as json | request.json['score']
      $('.add-word', this.board).hide();
      const resp = await axios.post('/post-score', { score: this.score });
      console.log(resp.data);
      if (resp.data.brokeRecord) {
         //shows as {brokeRecord:false}
         this.showMessage(`New record: ${this.score}`, 'ok');
      } else {
         this.showMessage(`Final score: ${this.score}`, 'ok');
      }
   }
}
