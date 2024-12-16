import {
  LitElement,
  html,
  css
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';


class RatingComponent extends LitElement {
  static properties = {
    // Component properties
    rating: { type: Number },
    comment: { type: String },
    // Component events
    sendRatingEvent: { type: String },
    // Others
    feedbackSent: {type: Boolean}
  };

  constructor() {
    super();
    // Component properties
    this.rating = -1;
    this.comment = '';
    // Compnent events
    this.sendRatingEvent = '';
    // Others
    this.feedbackSent = false;
  }

  static styles = css`
    :host {
      display: block;
      width: 200px; 
    }

    .star {
      cursor: pointer;
      font-size: 2rem;
      color: gray;
    }

    .star.selected {
      color: gold;
    }

    .container {
      display: flex;
      align-items: center;
      /* Hide the container initially */
      display: none; 
    }

    .container.show {
      display: flex; 
    }

    textarea {
      flex-grow: 1;
      padding: 10px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
      resize: none; 
    }

    .send-icon {
      font-size: 1.5rem;
      cursor: pointer;
      margin-left: 10px;
      color: #4CAF50; 
    }

    .send-icon.hide {
      display: none; 
    }
  `;


  render() {
    return html`
      <div>
        ${Array(5)
          .fill(0)
          .map((_, index) => html`
            <span 
              class="star ${index < this.rating ? 'selected' : ''}" 
              @click=${() => this.setRating(index + 1)}
            >
              &#9733;
            </span>
          `)}
      </div>
      <div class="container ${this.rating > 0 ? 'show' : ''}">
        <textarea 
          placeholder="Enter your comment" 
          @input=${(e) => this.comment = e.target.value}
          .value=${this.comment} 
          ?disabled=${this.feedbackSent} 
        ></textarea>
        <span class="send-icon ${this.feedbackSent ? 'hide' : ''}" @click=${this._onSendRating}>&#10003;</span>
      </div>
    `;
  }

  // hover(rating) {
  //   this.rating = rating;
  // }

  setRating(rating) {
    if (! this.feedbackSent) {
      this.rating = rating;
    }
    
  }

  _onSendRating() {
    this.dispatchEvent(
      new MesopEvent(this.sendRatingEvent, {
        rating: this.rating,
        comment: this.comment
      }),
    );

    this.feedbackSent = true

  }
}

customElements.define('rating-component', RatingComponent);