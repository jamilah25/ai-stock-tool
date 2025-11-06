import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

// Sample data for trading chart
const chartData = [
  { time: "09:00", value: 1.123 },
  { time: "09:30", value: 1.126 },
  { time: "10:00", value: 1.128 },
  { time: "10:30", value: 1.120 },
  { time: "11:00", value: 1.132 },
  { time: "11:30", value: 1.129 }
];

export default function AutomateCashApp() {
  const [balance, setBalance] = useState(1250.75);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">AutomateCash Trader</h1>
      <Tabs defaultValue="dashboard" className="max-w-4xl mx-auto">
        <TabsList className="grid grid-cols-4">
          <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
          <TabsTrigger value="market">Market</TabsTrigger>
          <TabsTrigger value="wallet">Wallet</TabsTrigger>
          <TabsTrigger value="profile">Profile</TabsTrigger>
        </TabsList>

        {/* Dashboard */}
        <TabsContent value="dashboard">
          <Card className="mt-6">
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-2">Welcome Back</h2>
              <p className="text-gray-600 mb-4">Your trading overview at a glance</p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Card className="p-4 text-center">
                  <p className="text-gray-500">Balance</p>
                  <p className="text-lg font-bold">${balance.toFixed(2)}</p>
                </Card>
                <Card className="p-4 text-center">
                  <p className="text-gray-500">Open Trades</p>
                  <p className="text-lg font-bold">3</p>
                </Card>
                <Card className="p-4 text-center">
                  <p className="text-gray-500">Profit/Loss</p>
                  <p className="text-lg font-bold text-green-600">+$32.45</p>
                </Card>
                <Card className="p-4 text-center">
                  <p className="text-gray-500">Referral Earnings</p>
                  <p className="text-lg font-bold">$10.00</p>
                </Card>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Market Tab */}
        <TabsContent value="market">
          <Card className="mt-6">
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4">Live EUR/USD Chart</h2>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
              <div className="mt-6 flex gap-2">
                <Button className="bg-green-600 text-white">Buy</Button>
                <Button className="bg-red-600 text-white">Sell</Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Wallet Tab */}
        <TabsContent value="wallet">
          <Card className="mt-6">
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4">Wallet Management</h2>
              <p className="text-gray-500 mb-4">Deposit or withdraw your funds easily.</p>
              <div className="flex gap-3 mb-4">
                <Input placeholder="Enter amount" type="number" className="max-w-xs" />
                <Button className="bg-green-600 text-white">Deposit</Button>
                <Button className="bg-yellow-500 text-white">Withdraw</Button>
              </div>
              <p className="text-gray-600">Connected Account: <strong>MTN Mobile Money</strong></p>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Profile Tab */}
        <TabsContent value="profile">
          <Card className="mt-6">
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4">Your Profile</h2>
              <p className="text-gray-600">Name: <strong>John Trader</strong></p>
              <p className="text-gray-600">Email: <strong>johntrader@example.com</strong></p>
              <p className="text-gray-600 mb-4">Verification: <span className="text-green-600 font-bold">Approved</span></p>
              <Button className="bg-gray-700 text-white">Edit Profile</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}