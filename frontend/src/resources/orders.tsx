import {
  List,
  Datagrid,
  TextField,
  DateField,
  Edit,
  SimpleForm,
  TextInput,
  SelectInput,
  Show,
  SimpleShowLayout,
} from "react-admin";
const statusChoices = [
  { id: "new", name: "new" },
  { id: "in_progress", name: "in_progress" },
  { id: "closed", name: "closed" },
  { id: "rejected", name: "rejected" },
];

export default function OrdersList() {
  return (
    <List>
      <Datagrid rowClick="edit">
        <TextField source="id" />
        <TextField source="status" />
        <TextField source="text" />
        <DateField source="created_at" />
      </Datagrid>
    </List>
  );
}

export const OrderShow = () => (
  <Show>
    <SimpleShowLayout>
      <TextField source="id" />
      <TextField source="status" />
      <TextField source="phone" />
      <DateField source="created_at" showTime />
      <DateField source="updated_at" showTime />
      <TextField source="text" />
      <TextField source="comment" />
    </SimpleShowLayout>
  </Show>
);

export const OrderEdit = () => (
  <Edit>
    <SimpleForm>
      <SelectInput source="status" choices={statusChoices} />
      <TextInput source="comment" fullWidth multiline />
    </SimpleForm>
  </Edit>
);
