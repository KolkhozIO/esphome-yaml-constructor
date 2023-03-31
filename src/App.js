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


const App = () => {
  const [formData, setFormData] = React.useState(null);
  const [hashData, setHashData] = React.useState({});
  const [seeData, setSseData] = React.useState([]);
  const serverBaseURL = "http://94.131.107.155:8000";

  //  Функция Post запрос compile, которая скачивает файл
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

//---------------------------------------------------------
//  Для переключения между JSON Form и Logs

  const [value, setValue] = React.useState('1');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };


//---------------------------------------------------------
//  Для внесения изменений в JSON Form и в форме с выводом yaml файла, так чтобы одно не сбрасывало другое

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
  function handleClick() {
    var yaml_text = JSON.stringify(formData);
    // Send data to the backend via POST
    fetch(`${serverBaseURL}/upload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: yaml_text // body data type must match "Content-Type" header
    })
    .then(response => response.json())
    .then(data => {
      console.log(data); // Выводим переменную hash_yaml в консоль браузера
      setHashData(data);
    })
    .catch(error => console.error(error));
  }

  function shareClick() {
    var yaml_text = JSON.stringify(formData)
    // Send data to the backend via POST
    fetch(`${serverBaseURL}/share`, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: yaml_text // body data type must match "Content-Type" header
    }).then(response=>response.json())
      .then(response=> console.log(response.json()))
  }

  //  сохранение введеных данных в форму
  useEffect(() => {
    const data = window.localStorage.getItem('MY_APP_STATE');
    if ( data !== null ) setFormData(JSON.parse(data));
  }, []);

  useEffect(() => {
    window.localStorage.setItem('MY_APP_STATE', JSON.stringify(formData));
  }, [formData]);


  function getLogs() {
    setSseData([]);
    fetch(`${serverBaseURL}/logs?hash_yaml=${hashData}`)
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




  return (
      <Grid container spacing={2}>
  <Grid item xs={6}>
    <button onClick={handleClick} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Upload
    </button>
    <button onClick={getLogs} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      logs
    </button>
    <button onClick={handleDownload} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      BIN
    </button>
    <button onClick={shareClick} style={{
      textAlign: 'center',
      width: '100px',
      border: '1px solid gray',
      borderRadius: '5px'
    }}>
      Share
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

export default App;