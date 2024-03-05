import * as _React from 'react'; 
import { styled } from '@mui/system'; 
import { Button, Typography, Stack } from '@mui/material';
import { Link } from 'react-router-dom'; 
import PokedexIcon from '@mui/icons-material/TravelExplore';
import BattleIcon from '@mui/icons-material/SportsKabaddi';
import TeamIcon from '@mui/icons-material/Groups3';


// internal import
import beforeHomeImage from '../../assets/images/home.jpg'; 
import afterHomeImage from '../../assets/images/afterhome.jpg'; 
import { NavBar } from '../sharedComponents';

interface Props {
    title: string
}

// code out our styled components
const Root = styled('div')({
    padding: 0,
    margin: 0
})

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'isLoggedIn' })<{
    isLoggedIn: boolean;
  }>(({ isLoggedIn }) => ({
    backgroundImage: `linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, .5)), url(${isLoggedIn ? afterHomeImage : beforeHomeImage})`,
    width: '100%',
    height: '100%',
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center bottom -81px',
    position: 'absolute',
    marginTop: '10px'
  }));
  
  const MainText = styled('div')({
    textAlign: 'center',
    position: 'relative',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    color: 'white'
  });
  
  // This is our first functional based component!
  export const Home = (props: Props) => {
      const myAuth = localStorage.getItem('auth');
  

      // Content to display if the user is logged in
      const loggedInContent = (
          <Stack direction="row" spacing={2} justifyContent="center">
              <Button startIcon={<PokedexIcon />} component={Link} to="/pokedex" variant='contained'>
                  Pokedex
              </Button>
              <Button startIcon={<BattleIcon />} component={Link} to="/battles" variant='contained'>
                  Battles
              </Button>
              <Button startIcon={<TeamIcon />} component={Link} to="/team-management" variant='contained'>
                  Team Management
              </Button>
          </Stack>
      );
  
      // Content to display if the user is not logged in
      const loggedOutContent = (
          <Button sx={{ marginTop: '10px' }} component={Link} to="/auth" variant='contained'>
              The Best of the Best Awaits. Enter when ready....
          </Button>
      );
  
      // Pass isLoggedIn prop to Main
      return (
          <Root>
              <NavBar /> 
              <Main isLoggedIn={myAuth === 'true'}>
                  <MainText>
                      <Typography variant='h3'>{props.title}</Typography>
                      {/* Conditional rendering based on auth status */}
                      {myAuth === 'true' ? loggedInContent : loggedOutContent}
                  </MainText>
              </Main>
          </Root>
      );
  };