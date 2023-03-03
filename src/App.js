import validator from "@rjsf/validator-ajv8";
import schema from './schema.json';
import Form from "@rjsf/mui";
import { Grid } from '@mui/material';
import YAML from 'yaml';
import * as React from 'react';
import { useEffect } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';


const App = () => {
  const [formData, setFormData] = React.useState(null);
  const [uuidData, setUuidData] = React.useState();

  useEffect(() => {
    const data = window.localStorage.getItem('MY_APP_STATE');
    if ( data !== null ) setFormData(JSON.parse(data));
  }, []);

  useEffect(() => {
    window.localStorage.setItem('MY_APP_STATE', JSON.stringify(formData));
  }, [formData]);
//  const [val, setVal] = React.useState(YAML.stringify(formData));
//  const onChange = (e) => {
//    setVal(e.target.value);
//  };

  function handleClick() {
    var yaml_text = JSON.stringify(formData)
    // Send data to the backend via POST
    fetch('http://localhost:8000/upload', {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: yaml_text // body data type must match "Content-Type" header
    })
  }

  function shareClick() {
    var yaml_text = JSON.stringify(formData)
    // Send data to the backend via POST
    fetch('http://localhost:8000/share', {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: yaml_text // body data type must match "Content-Type" header
    }).then(response=>response.json())
      .then(response=> setUuidData(response.json()))
  }
  return (
      <Grid container spacing={2}>
  <Grid item xs={6}>
    <Box
      component="form"
      sx={{
          '& .MuiTextField-root': { m: 1, width: '100ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <div>
        <TextField
          id="standard-multiline-static"
          multiline
          rows={50}
          variant="standard"
          value={YAML.stringify(formData)}
          onChange={e => setFormData(e.formData)}
        />
      </div>
    </Box>
    <button onClick={handleClick} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Send data to backend
    </button>
    <Typography variant={'h4'}>
      <pre>{JSON.stringify(uuidData)}</pre>
    </Typography>
    <button onClick={shareClick} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Share
    </button>
  </Grid>
  <Grid item xs={6}>
    <Form
      schema={schema}
      formData={formData}
      onChange={e => setFormData(e.formData)}
      validator={validator}
    />
  </Grid>
</Grid>


  );
};

export default App;