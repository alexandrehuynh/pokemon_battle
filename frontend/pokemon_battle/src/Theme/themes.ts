import { createTheme } from'@mui/material'; 
import shopImage from '../assets/images/login.jpg'; 


export const theme = createTheme({
    typography: {
        fontFamily: 'Inter, system-ui, Avenir, Helvetica, Arial, sans-serif'
    },
    palette: {
        primary: {
            main: '#00794E'
        },
        secondary: {
            main: '#242625',
            light: '#1B2929'
        },
        info: {
            main: '#44469D'
        }
    }
})


// creating our dictionary/object for our css styling 

export const authStyles = {
    main: {
        backgroundImage: `linear-gradient(rgba(0, 0, 0, .3), rgba(0, 0, 0, .5)), url(${shopImage});`,
        width: '100%',
        height: '100%',
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center bottom -20px', 
        position: 'absolute',
        marginTop: '10px'
    },
    stack: {
        width: '400px',
        marginTop: '100px',
        marginRight: 'auto', //used a lot to center your div
        marginLeft: 'auto',
        color: 'white'
    },
    button: {
        width: '175px',
        fontSize: '14px'
    }
}