import type { Meta, StoryObj } from "@storybook/react";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";

const meta = {
  title: "UI/Input",
  component: Input,
  tags: ["autodocs"],
  argTypes: {
    type: {
      control: "select",
      options: ["text", "email", "password", "number", "search", "tel", "url"],
    },
    disabled: { control: "boolean" },
    placeholder: { control: "text" },
  },
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    placeholder: "Enter text...",
    type: "text",
  },
};

export const Email: Story = {
  args: {
    placeholder: "user@example.com",
    type: "email",
  },
};

export const Password: Story = {
  args: {
    placeholder: "Enter password",
    type: "password",
  },
};

export const Disabled: Story = {
  args: {
    placeholder: "Disabled input",
    disabled: true,
  },
};

export const WithValue: Story = {
  args: {
    defaultValue: "Hello World",
  },
};

export const File: Story = {
  args: {
    type: "file",
  },
};

export const NeonForge: Story = {
  name: "Neon Forge Search",
  render: () => (
    <div className="flex items-center gap-2 w-[400px] bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[21px] px-5 py-2.5">
      <Search className="w-4 h-4 text-[var(--nf-muted)]" />
      <input
        className="bg-transparent text-sm text-[var(--nf-white)] placeholder:text-[var(--nf-muted)] outline-none flex-1"
        placeholder="搜索"
      />
    </div>
  ),
};

export const AllTypes: Story = {
  name: "All Types",
  render: () => (
    <div className="flex flex-col gap-3 w-[300px]">
      <Input placeholder="Text input" type="text" />
      <Input placeholder="Email input" type="email" />
      <Input placeholder="Password input" type="password" />
      <Input placeholder="Number input" type="number" />
      <Input placeholder="Search input" type="search" />
      <Input type="file" />
    </div>
  ),
};
