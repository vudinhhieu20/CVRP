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
  Row,
  Col,
  Table,
} from "antd";
import { UploadOutlined } from "@ant-design/icons";
import axios from "axios";

function FileForm() {
  const [file, setFile] = useState(null);
  const [listBusStopCoord, setListBusStopCoord] = useState([]);
  const [listAssignBusStop, setListAssignBusStop] = useState([]);
  const [listRoutesGreedy, setListRoutesGreedy] = useState([]);
  const [listRoutesSaving, setListRoutesSaving] = useState([]);
  const [listRoutes, setListRoutes] = useState([]);

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

    console.log(formData);
    try {
      // post request
      const url = "http://127.0.0.1:8000/cvrp/upload_file/";
      const response = await axios.post(url, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log(response);
      if (response.status === 200) {
        let customListBusStopCoord = response.data["bus_stop_coord"].map(
          (item, index) => ({
            number: index + 1,
            coord: item.join(", "),
          })
        );
        let customListAssignBusStop = response.data["bus_stop_assign"].map(
          (item) => ({
            id: item[0],
            busStop: item[1],
          })
        );
        let routesGreedy = response.data["routes"]["routes_greedy"]
        let routesSaving = response.data["routes"]["routes_saving"]

        let routesGreedyStr = '['
        for (let route of routesGreedy){
          routesGreedyStr +=' [ '+route.join(', ') + '], '
        }
        routesGreedyStr += ']'

        let routesSavingStr = '['
        for (let route of routesSaving){
          routesSavingStr +=' [ '+route.join(', ') + '], '
        }
        routesSavingStr += ']'

        let customListRoutes = [
          {
            id: 1,
            routes: routesGreedyStr,
          },
          {
            id: 2,
            routes: routesSavingStr,
          },
        ];
        
        setListBusStopCoord(customListBusStopCoord);
        setListAssignBusStop(customListAssignBusStop);
        setListRoutesGreedy(response.data["routes"]["routes_greedy"]);
        setListRoutesSaving(response.data["routes"]["routes_saving"]);
        setListRoutes(customListRoutes);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const columnsListBusStop = [
    {
      title: "STT",
      dataIndex: "number",
      key: "number",
      render: (text) => <span>{text}</span>,
    },
    {
      title: "Tạo độ",
      dataIndex: "coord",
      key: "coord",
      render: (text) => <span>{text}</span>,
    },
  ];

  const columnsListAssignBusStop = [
    {
      title: "Mã học sinh",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Điểm bus",
      dataIndex: "busStop",
      key: "busStop",
    },
  ];

  const columnsListRoutes = [
    {
      title: "STT",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Lộ trình gợi ý",
      dataIndex: "routes",
      key: "routes",
    },
  ];

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
          onFinish={(value) => handleSubmit(value)}
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
            <Button type="primary" htmlType="submit" label="">
              Submit
            </Button>
          </Form.Item>
        </Form>
        {/* <Button type="primary" onClick={handleSubmit}>
          Primary Button
        </Button> */}

        <Row gutter={16}>
          <Col className="gutter-row" span={12}>
            <h3>Danh sách điểm bus</h3>
            <Table columns={columnsListBusStop} dataSource={listBusStopCoord} />
            ;
          </Col>
          
          <Col className="gutter-row" span={12}>
            <h3>Danh sách phân chia học sinh các điểm bus</h3>
            <Table
              columns={columnsListAssignBusStop}
              dataSource={listAssignBusStop}
            />
            ;
          </Col>
          <Col className="gutter-row" span={24}>
            <h3>Danh sách lộ trình gợi ý</h3>
            <Table columns={columnsListRoutes} dataSource={listRoutes} />
          </Col>
        </Row>
      </div>
    </>
  );
}

export default FileForm;
