import validator from "@rjsf/validator-ajv8";
import schema from './schema.json';
import Form from "@rjsf/mui";
//import Form from "@rjsf/core";
//import Form from "@rjsf/material-ui";
import { Grid } from '@mui/material';
import YAML from 'yaml';
import * as React from 'react';
import { useEffect } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
//import { styled } from '@mui/system';
//import TabsUnstyled from '@mui/base/TabsUnstyled';
//import TabsListUnstyled from '@mui/base/TabsListUnstyled';
//import TabPanelUnstyled from '@mui/base/TabPanelUnstyled';
//import { buttonUnstyledClasses } from '@mui/base/ButtonUnstyled';
//import TabUnstyled, { tabUnstyledClasses } from '@mui/base/TabUnstyled';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import { fetchEventSource } from '@microsoft/fetch-event-source';


const App = () => {
  const [formData, setFormData] = React.useState(null);
  const [uuidData, setUuidData] = React.useState();
  const [hashData, setHashData] = React.useState({});
//  const [binData, setBinData] = React.useState();
  const serverBaseURL = "http://localhost:8000";
  const handleFormChange = ({formData}) => {
    setFormData(formData);
  };

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
      headers: { 'Content-Type': 'application/json' },
      body: yaml_text // body data type must match "Content-Type" header
    }).then(response => response.json())
      .then(data => setHashData(data))
  }


//  function handleDownloadFile() {
//    fetch(`${serverBaseURL}/compile?hash_yaml=${hashData}`, {
//      method: 'POST',
//      headers: {
//        'Content-Type': 'application/json'
//      }
//    })
//    .then(response => {
//      return response.blob();
//    })
//    .then(blob => {
//      const file = new File([blob], 'example.bin', { type: 'application/json' });
//      // Обработка файла
//      console.log(file);
//    })
//    .catch(error => {
//      console.error(error);
//    });
//  }

  const handleDownload = () => {
    fetch(`${serverBaseURL}/compile?hash_yaml=${hashData}`, {
      method: 'POST'
    })
      .then(response => response.blob())
      .then(blob => {
        // Сохраняем бинарный файл как object URL
        const url = URL.createObjectURL(blob);

        // Создаем ссылку для скачивания файла
        const link = document.createElement('a');
        link.href = url;
        link.download = 'file.bin';

        // Програмно кликаем по ссылке, чтобы начать скачивание
        link.click();
      });
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
      .then(response=> console.log(response.json()))
  }


  const [seeData, setSseData] = React.useState([]);
  const fetchData = async () => {
    setSseData([]);
    const res = await fetchEventSource(`${serverBaseURL}/logs?hash_yaml=${hashData}`,
      {
        method: "GET",
        onopen(res) {
          if (res.ok && res.status === 200) {
            console.log("Connection Established", res);
          } else if (
            res.status >= 400 &&
            res.status < 500 &&
            res.status !== 429
          ) {
            console.log("Client Side Failure", res);
          }
        },
        onmessage(event) {
          console.log(event.data);
          setSseData(prevData => prevData.concat(event.data));
        },
        onclose() {
          console.log("Connection Closed by the Server");
        },
        onerror(err) {
          console.log("There was an error from the Server!", err);
        },
      }
    );
  };



//---------------------------------------------------------


  const [value, setValue] = React.useState('1');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };


//---------------------------------------------------------







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
          onChange={handleFormChange}
        />
      </div>
    </Box>
    <button onClick={handleClick} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Upload
    </button>
    <button onClick={fetchData} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      logs
    </button>
    <button onClick={shareClick} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Share
    </button>
    <button onClick={handleDownload} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      BIN
    </button>
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
        <TabPanel value="2">{seeData}</TabPanel>
      </TabContext>
    </Box>
  </Grid>
</Grid>


  );
};

export default App;