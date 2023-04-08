import validator from "@rjsf/validator-ajv8";
import schema from './schema.json';
import Form from "@rjsf/mui";
import { Grid } from '@mui/material';
import YAML from 'yaml';
import * as React from 'react';
import { useEffect } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams,
} from 'react-router-dom';


const App = () => {
  const [formData, setFormData] = React.useState(null);
  const [hashData, setHashData] = React.useState({});
  const [seeData, setSseData] = React.useState([]);
  const serverBaseURL = process.env.API_URL;
  const serverFrontBaseURL = process.env.APP_URL;

  function handleClick() {
    setSseData([]);
    var yaml_text = JSON.stringify(formData);
    // Send data to the backend via POST
    fetch(`${serverBaseURL}/compile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: yaml_text // body data type must match "Content-Type" header
    })
    .then(response => {
      const reader = response.body.getReader();
      let partial = '';
      return reader.read().then(function processResult(result) {
        const text = partial + new TextDecoder().decode(result.value || new Uint8Array, {stream: !result.done});
        const lines = text.split(/\r?\n/);
        partial = lines.pop() || '';
        console.log(lines.join('\n')); // вывод логов в консоль
        setSseData(prevData => [...prevData, ...lines]); // добавить логи в состояние
        if (result.done) {
          return;
        }
        return reader.read().then(processResult);
      });
    })
    .catch(error => {
      console.error(error);
    });
  }

  function getLogsValidate() {
    setSseData([]);
    var yaml_text = JSON.stringify(formData);
    fetch(`${serverBaseURL}/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: yaml_text
    })
    .then(response => {
      const reader = response.body.getReader();
      let partial = '';
      return reader.read().then(function processResult(result) {
        const text = partial + new TextDecoder().decode(result.value || new Uint8Array, {stream: !result.done});
        const lines = text.split(/\r?\n/);
        partial = lines.pop() || '';
        console.log(lines.join('\n')); // вывод логов в консоль
        setSseData(prevData => [...prevData, ...lines]); // добавить логи в состояние
        if (result.done) {
          return;
        }
        return reader.read().then(processResult);
      });
    })
    .catch(error => {
      console.error(error);
    });
  }

  //  Post request compile function that downloads a file
  const handleDownload = () => {
    var yaml_text = JSON.stringify(formData);
    fetch(`${serverBaseURL}/download`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: yaml_text
    })
      .then(response => response.blob())
      .then(blob => {
        // Saving the binary file as an object URL
        const url = URL.createObjectURL(blob);

        // Create a link to download a file
        const link = document.createElement('a');
        link.href = url;
        link.download = 'file.bin';

        // Programmatically click on the link to start the download
        link.click();
      });
  }

//---------------------------------------------------------
//  To switch between JSON Form and Logs

  const [value, setValue] = React.useState('1');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

//---------------------------------------------------------
//  To make changes to a JSON Form and a yaml output form so that one doesn't override the other

  const [textAreaValue, setTextAreaValue] = React.useState(YAML.stringify(formData));

  const handleFormChange = ({ formData }) => {
    setFormData(formData);
    setTextAreaValue(YAML.stringify(formData));
  }

  const handleTextAreaChange = (event) => {
    const value = event.target.value;
    setTextAreaValue(value);

    try {
      const parsedData = YAML.parse(value);
      setFormData(parsedData);
    } catch (error) {
      console.error('Error parsing YAML', error);
      // Handle parse error, e.g. show error message to user.
    }
  }

//---------------------------------------------------------

  //  save the entered data in the form
  useEffect(() => {
    const data = window.localStorage.getItem(`MY_APP_STATE_${window.location.pathname}`);
    if (data !== null) setFormData(JSON.parse(data));
  }, []);

  useEffect(() => {
    window.localStorage.setItem(`MY_APP_STATE_${window.location.pathname}`, JSON.stringify(formData));
  }, [formData]);

//---------------------------------------------------------
  // Share

  const [uuidData, setUuidData] = React.useState({});
  const [sharedLink, setSharedLink] = React.useState('');
  function handleLinkClick() {
    var json_text = JSON.stringify(formData);
    fetch(`${serverBaseURL}/share`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: json_text
    })
    .then(response => response.json())
    .then(data => {
      // Save the shared link and update state
      setSharedLink(data.url);
    })
    .catch(error => {
      console.error(error);
    });
  }

  function displayChareFileData(uuid) {
    fetch(`${serverBaseURL}/share?file_name=${uuid}`, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      // Update the state with the retrieved data
      console.log(data.json_text)
      setFormData(data.json_text);
    })
    .catch(error => {
      console.error(error);
    });
  }

  // getting information from the database if the url has a uuid
  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const uuid = searchParams.get('uuid');
    if (uuid) {
      displayChareFileData(uuid);
    }
  }, []);


//---------------------------------------------------------


  const openDeviceSession = async () => {
  try {
    const device = await navigator.usb.requestDevice({
      filters: []
    });
    await device.open();
    await device.selectConfiguration(1);
    await device.claimInterface(0);
    console.log('Device session opened');
  } catch (error) {
    console.error('Error opening device session:', error);
  }
  };



  return (
      <Grid container spacing={2}>
  <Grid item xs={6}>
  <button onClick={getLogsValidate} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Validate
    </button>
    <button onClick={handleClick} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Compile
    </button>
    <button onClick={handleDownload} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Download BIN
    </button>
    <button onClick={openDeviceSession} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Connect to device
    </button>
    <Box
      component="form"
      sx={{
          '& .MuiTextField-root': { m: 1, width: '90ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <div>
        <TextField
          id="standard-multiline-static"
          multiline
          rows={48}
          variant="standard"
          value={textAreaValue}
          onChange={handleTextAreaChange}
        />
      </div>
    </Box>
    <button onClick={handleLinkClick}>Share Link</button>
      {sharedLink && (
        <a href={sharedLink}>
          {sharedLink}
        </a>
      )}
  </Grid>
  <Grid item xs={6}>
    <Box sx={{ width: '100%', typography: 'body1' }}>
      <TabContext value={value}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <TabList onChange={handleChange} aria-label="lab API tabs example">
            <Tab label="Json Form" value="1" />
            <Tab label="Logs" value="2" />
          </TabList>
        </Box>
        <TabPanel value="1">
        <Form
          schema={schema}
          formData={formData}
          onChange={handleFormChange}
          validator={validator}
        />
        </TabPanel>
        <TabPanel value="2">
          {seeData.map((line, index) => (
            <div key={index}>{line}</div>
          ))}
        </TabPanel>
      </TabContext>
    </Box>
  </Grid>
</Grid>


  );
};

const About = () => <h2>Контакты</h2>;

export default App;