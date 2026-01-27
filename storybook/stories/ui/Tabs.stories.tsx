import type { Meta, StoryObj } from "@storybook/react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";

const meta = {
  title: "UI/Tabs",
  component: Tabs,
  tags: ["autodocs"],
} satisfies Meta<typeof Tabs>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Tabs defaultValue="tab1" className="w-[400px]">
      <TabsList>
        <TabsTrigger value="tab1">Account</TabsTrigger>
        <TabsTrigger value="tab2">Password</TabsTrigger>
        <TabsTrigger value="tab3">Settings</TabsTrigger>
      </TabsList>
      <TabsContent value="tab1">
        <p className="text-sm text-muted-foreground p-4">Account settings content.</p>
      </TabsContent>
      <TabsContent value="tab2">
        <p className="text-sm text-muted-foreground p-4">Password settings content.</p>
      </TabsContent>
      <TabsContent value="tab3">
        <p className="text-sm text-muted-foreground p-4">General settings content.</p>
      </TabsContent>
    </Tabs>
  ),
};

export const LineVariant: Story = {
  name: "Line Variant",
  render: () => (
    <Tabs defaultValue="tab1" className="w-[400px]">
      <TabsList variant="line">
        <TabsTrigger value="tab1">Overview</TabsTrigger>
        <TabsTrigger value="tab2">Analytics</TabsTrigger>
        <TabsTrigger value="tab3">Reports</TabsTrigger>
      </TabsList>
      <TabsContent value="tab1">
        <p className="text-sm text-muted-foreground p-4">Overview content.</p>
      </TabsContent>
      <TabsContent value="tab2">
        <p className="text-sm text-muted-foreground p-4">Analytics content.</p>
      </TabsContent>
      <TabsContent value="tab3">
        <p className="text-sm text-muted-foreground p-4">Reports content.</p>
      </TabsContent>
    </Tabs>
  ),
};

export const Vertical: Story = {
  render: () => (
    <Tabs defaultValue="tab1" orientation="vertical" className="w-[400px]">
      <TabsList>
        <TabsTrigger value="tab1">General</TabsTrigger>
        <TabsTrigger value="tab2">Security</TabsTrigger>
        <TabsTrigger value="tab3">Notifications</TabsTrigger>
      </TabsList>
      <TabsContent value="tab1">
        <p className="text-sm text-muted-foreground p-4">General settings.</p>
      </TabsContent>
      <TabsContent value="tab2">
        <p className="text-sm text-muted-foreground p-4">Security settings.</p>
      </TabsContent>
      <TabsContent value="tab3">
        <p className="text-sm text-muted-foreground p-4">Notification preferences.</p>
      </TabsContent>
    </Tabs>
  ),
};

export const NeonForge: Story = {
  name: "Neon Forge Style",
  render: () => (
    <Tabs defaultValue="hot" className="w-[500px]">
      <TabsList variant="line">
        <TabsTrigger value="hot">热门</TabsTrigger>
        <TabsTrigger value="proposals">提案广场</TabsTrigger>
        <TabsTrigger value="resources">资源</TabsTrigger>
        <TabsTrigger value="teams">找队友</TabsTrigger>
      </TabsList>
      <TabsContent value="hot">
        <p className="text-sm text-[var(--nf-muted)] p-4">热门内容展示区域</p>
      </TabsContent>
      <TabsContent value="proposals">
        <p className="text-sm text-[var(--nf-muted)] p-4">提案广场内容</p>
      </TabsContent>
      <TabsContent value="resources">
        <p className="text-sm text-[var(--nf-muted)] p-4">资源内容</p>
      </TabsContent>
      <TabsContent value="teams">
        <p className="text-sm text-[var(--nf-muted)] p-4">找队友内容</p>
      </TabsContent>
    </Tabs>
  ),
};
