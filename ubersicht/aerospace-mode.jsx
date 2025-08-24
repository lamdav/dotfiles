// AeroSpace Mode Indicator for Übersicht
// Shows current AeroSpace mode with SpaceDuck theme styling

export const refreshFrequency = 1000;

export const command = "/Users/lamdav/configs/dotfiles/ubersicht/simple-bar/aerospace-mode-tracker.sh get";

export const render = ({ output }) => {
  const mode = output ? output.trim() : 'main';
  
  return (
    <div className={`aerospace-mode ${mode}`}>
      {mode.toUpperCase()}
    </div>
  );
};

export const className = `
  .aerospace-mode {
    position: fixed;
    top: 6px;
    left: 50%;
    transform: translateX(-200px);
    z-index: 9999;
    font-family: 'FiraCode Nerd Font', 'JetBrains Mono', Monaco, Menlo, monospace;
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    min-width: 60px;
    text-align: center;
    border-radius: 20px;
    padding: 6px 14px;
    margin: 0 4px;
    transition: all 0.2s ease;
  }
  
  .aerospace-mode.main {
    background-color: #1b1c36;
    color: #ecf0c1;
  }
  
  .aerospace-mode.media {
    background-color: #1db954;
    color: #0f111b;
  }
  
  .aerospace-mode.resize {
    background-color: #f2ce00;
    color: #0f111b;
  }
  
  .aerospace-mode.service {
    background-color: #e33400;
    color: #0f111b;
  }
`;