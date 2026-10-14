"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

export default function LoginPage() {
  const [email, setEmail] = useState("asha@meridian.example.test");
  const [password, setPassword] = useState("Sitewise-Demo-1234");
  const [err, setErr] = useState("");
  const router = useRouter();
  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold">Welcome back</CardTitle>
          <CardDescription>Sign in to your Sitewise account</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />
          </div>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="password">Password</Label>
            </div>
            <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" />
          </div>
          {err && <p className="text-sm text-destructive">{err}</p>}
          <Button className="w-full" onClick={() => login(email, password).then(() => router.push("/cases")).catch((e) => setErr(e.message))}>
            Sign in
          </Button>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <Separator />
          <p className="text-xs text-center text-muted-foreground">
            Seeded emails end in <code className="bg-muted px-1 rounded">.example.test</code> · password <code className="bg-muted px-1 rounded">Sitewise-Demo-1234</code>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}