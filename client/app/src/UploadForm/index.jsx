import { useState, useEffect } from "react";
import {
    Box,
    Heading,
    Container,
    Text,
    Button,
    Stack,
    Input,
    Select
} from '@chakra-ui/react';
import * as XLSX from "xlsx";

import postData from '../utility/postData';
// import CodeTable from "../CodeTable";

export default function UploadForm() {

    const [show, setShow] = useState(false);
    const [sheets, setSheets] = useState([]);
    const [b, setB] = useState();
    const [cols, setCols] = useState([]);
    const [selectedSheet, setSelectedSheet] = useState("");
    const [payload, setPayload] = useState([]);
    const [data, setData] = useState();

    /* useEffect(() => {
      console.log(data);
    }, [data]);
  */



    const onFileChange = (e) => {
        const [file] = e.target.files;
        const reader = new FileReader();
        reader.onload = (evt) => {
            const bstr = evt.target.result;
            const wb = XLSX.read(bstr, { type: "binary" });
            setB(wb);
            const rawSheets = wb.SheetNames;
            setSheets(rawSheets);

        };
        reader.readAsBinaryString(file);
        //e.target.value = null;
    };

    /* extract column:
    for (const i of l){
      if (Object.keys(i) == k) {
        console.log(Object.values(i))
        }
    }
    */
    const onSheetChange = (e) => {
        if (e.target.value) {
            const ws = b.Sheets[e.target.value];
            const data = XLSX.utils.sheet_to_json(ws, { header: 1 });
            setSelectedSheet(e.target.value)
            setCols(data[0]);

        }
    };




    const onColChange = (e) => {
        if (e.target.value) {
            const ws = b.Sheets[selectedSheet];
            const data = XLSX.utils.sheet_to_json(ws, { header: 2 });
            const colName = e.target.value;
            setPayload(data.map(function (el) { return el[colName] }));
        }


    };

    const submitHandler = (e) => {
        e.preventDefault();
        postData('api/files/clientsearch', payload).then(
            response => {
                response.blob().then(blob => {
                    let url = window.URL.createObjectURL(blob);
                    let a = document.createElement("a");
                    console.log(url);
                    a.href = url;
                    a.download = "test.csv";
                    a.click();
                });
            });

        //promise.then(setData);
        //setShow(true);
        //data ? console.log(data) : console.log("loading...");
    };

    return (
        <>
            {/* <Head>
                <link
                    href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap"
                    rel="stylesheet"
                />
            </Head> */}

            <Container maxW={'3xl'}>
                <Stack
                    as={Box}
                    textAlign={'center'}
                    spacing={{ base: 8, md: 14 }}
                    py={{ base: 20, md: 36 }}>
                    {/* <Heading
            fontWeight={600}
            fontSize={{ base: '2xl', sm: '4xl', md: '6xl' }}
            lineHeight={'110%'}>
            Title <br />
          </Heading>
          <Text color={'gray.500'}>
            Subtitle
          </Text> */}
                    <Stack
                        direction={'column'}
                        spacing={3}
                        align={'center'}
                        alignSelf={'center'}
                        position={'relative'}>
                        <form onSubmit={submitHandler}>
                            <Input type="file" onChange={onFileChange} />
                            <Select placeholder='Select Sheet' onChange={onSheetChange}>
                                {sheets.map((sheet, key) => {
                                    return <option value={sheet} key={key}>{sheet}</option>;
                                })}
                            </Select>
                            <Select placeholder='Select Column' onChange={onColChange}>
                                {cols.map((col, key) => {
                                    return <option value={col} key={key}>{col}</option>;
                                })}
                            </Select>
                            <Button variant={'link'} colorScheme={'blue'} size={'sm'} type="submit">
                                s u b m i t
                            </Button>
                        </form>
                        {/* {show && data ? <CodeTable data={data} /> : <div />} */}
                    </Stack>
                </Stack>
            </Container>
        </>
    );
}
