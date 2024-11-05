# KeySound

A Python application that plays sound frequencies corresponding to keyboard events, enhancing the typing experience with audio feedback.

## Features

- Plays different sounds for various key types (letters, Enter, Space, Backspace, Shift).
- Customizable sound frequencies and volume levels.
- Smooth sound envelope with attack and decay effects.
- Keyboard event listening using `pynput`.
- Simple installation and usage.

## Installation

To run the KeySound, you'll need Python and the following libraries:

- `numpy`
- `pyaudio`
- `pynput`

You can install the required libraries using pip:

```bash
pip install numpy pyaudio pynput


## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/HouwyTwitch/KeySound.git
   cd KeySound
   ```

2. Run the application:

   ```bash
   python main.py
   ```

3. Press keys on your keyboard to hear sounds corresponding to your keystrokes. 
4. To exit the application, press `Ctrl + Shift + Q`.

## Example

Here’s how the sound mapping works:

- **Letters**: 400 Hz
- **Enter**: 350 Hz
- **Space**: 320 Hz
- **Backspace**: 450 Hz
- **Shift**: 370 Hz

Feel free to customize the sound frequencies and volume in the code as needed.

## Contributing

Contributions are welcome! If you would like to improve this project, please fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Open a pull request.
