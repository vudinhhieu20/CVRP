import React, { useState } from "react";
import {
  Button,
  Cascader,
  Checkbox,
  ColorPicker,
  DatePicker,
  Form,
  Input,
  InputNumber,
  Radio,
  Select,
  Slider,
  Switch,
  TreeSelect,
  Upload,
} from "antd";
import { UploadOutlined } from "@ant-design/icons";
import axios from "axios";

function FileForm() {
  const [file, setFile] = useState(null);
  const [maxStudent, setMaxStudent] = useState(0);
  const [maxCapacity, setMaxCapacity] = useState(0);
  const [maxDistance, setMaxDistance] = useState(0);

  const [form] = Form.useForm();

  const handleFileInputChange = (e) => {
    console.log(e.targe);
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (value) => {
    // e.preventDefault();

    const formData = new FormData();
    formData.append("file_upload", file);
    formData.append("max_student", parseInt(value.max_student));
    formData.append("max_capacity", parseInt(value.max_capacity));
    formData.append("max_distance", parseInt(value.max_distance));

    console.log(formData)
    try {
      // post request
      const url = "http://127.0.0.1:8000/cvrp/upload_file/";
      const response = await axios.post(url, formData, { headers: { 'Content-Type': 'multipart/form-data'}});
      console.log(response);
      if (response.status === 200) {
        console.log("HHHHHHHHHHHHHHHHH");
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div>
        <h1>Upload file</h1>
        <Form
          labelCol={{
            span: 12,
          }}
          wrapperCol={{
            span: 12,
          }}
          layout="horizontal"
          style={{
            maxWidth: 600,
          }}
          form={form}
          onFinish={value => handleSubmit(value)}
        >
          <Form.Item
            label="Max number student for each bus stop"
            name="max_student"
          >
            <InputNumber />
          </Form.Item>
          <Form.Item
            label="Max distance from student to bus stop"
            name="max_distance"
          >
            <InputNumber />
          </Form.Item>
          <Form.Item label="Max bus capacity" name="max_capacity">
            <InputNumber />
          </Form.Item>

          <Form.Item label="Upload" valuePropName="fileList">
            <input type="file" onChange={handleFileInputChange} />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" label="">Submit</Button>
          </Form.Item>
        </Form>
        {/* <Button type="primary" onClick={handleSubmit}>
          Primary Button
        </Button> */}
      </div>
    </>
  );
}

export default FileForm;
