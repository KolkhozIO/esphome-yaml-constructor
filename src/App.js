import validator from "@rjsf/validator-ajv8";
import schema from './schema.json';
import React from "react";
import Form from "@rjsf/mui";
import { Grid } from '@mui/material';
import YAML from 'yaml';
import Typography from '@mui/material/Typography';


const App = () => {
  const [formData, setFormData] = React.useState(null);
  function handleClick() {
    var file = new FormData();
    var file_yaml = YAML.stringify(formData)
    file.append("file", file_yaml)

    console.log(file)
    // Send data to the backend via POST
    fetch('http://localhost:8000/uploadd', {

      method: 'POST',
      mode: 'no-cors',
      body: file // body data type must match "Content-Type" header

    })

  }
  return (
      <Grid container spacing={2}>
  <Grid item xs={6}>
    <Typography variant={'h4'}>
      <pre>{YAML.stringify(formData)}</pre>
    </Typography>
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