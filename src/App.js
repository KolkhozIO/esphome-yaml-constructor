import validator from "@rjsf/validator-ajv8";
import schema from './schema.json';
import React from "react";
import Form from "@rjsf/mui";
import { Grid } from '@mui/material';
import YAML from 'yaml';
import Typography from '@mui/material/Typography';


const App = () => {
  const [formData, setFormData] = React.useState(null);
  return (
      <Grid container spacing={2}>
  <Grid item xs={6}>
    <Typography variant={'h4'}>
      <pre>{YAML.stringify(formData)}</pre>
    </Typography>
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