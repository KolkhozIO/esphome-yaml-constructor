import validator from "@rjsf/validator-ajv8";
import schema from './schema.json';
//import React from "react";
import Form from "@rjsf/mui";
import { Grid } from '@mui/material';
import YAML from 'yaml';
//import { Editor } from 'draft-js';
//import Typography from '@mui/material/Typography';
import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';


const App = () => {
  const [formData, setFormData] = React.useState(null);
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